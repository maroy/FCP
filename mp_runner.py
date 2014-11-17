import os
import time
import yaml
import Orange
import multiprocessing
import cPickle


def process_print(message):
    print "[{0}] {1}".format(os.getpid(), message)

def run(test_file, output_path, console_lock, pickled_classifier_path):

    with console_lock:
        classifier = cPickle.load(open(pickled_classifier_path, 'rb'))

    test = Orange.data.Table(test_file)

    count = 0

    with open(output_path, 'w') as out_file:
        out_file.write('Id,Cover_Type\n')
        for s in test:

            out_file.write("{0},{1}\n".format(s["Id"].value, classifier.classify(s)))
            count += 1

            if count % 1000 == 0:
                with console_lock:
                    process_print("processed {0}/{1} items".format(count, len(test)))
        process_print("processed {0}/{1} items".format(count, len(test)))


def partition_test_data(test_path, count):
    with open(test_path, "rb") as f:
        lines = f.readlines()

    split_files = []
    headers = lines[:3]
    start = 3
    for i in range(0, count):
        split_files.append("tmp/mp_test_{0}.tab".format(i+1))
        with open(split_files[-1], "wb") as f:
            f.writelines(headers)
            end = len(lines) if i == count - 1 else start + len(lines) / count
            for j in range(start, end):
                f.write(lines[j])
            start = end

    return split_files


def main():

    if not os.path.isdir("tmp"):
        os.mkdir("tmp")
    else:
        for f in os.listdir("tmp"):
            os.remove("tmp/" + f)

    start_time = time.time()

    with open("mp_runner.yaml", "rb") as f:
        config = yaml.load(f)

    training_file = config["training_file"]
    test_file = config["test_file"]
    classifier_module = config["classifier_module"]
    process_count = config["process_count"]
    pickled_classifier_path = config["pickled_classifier_path"]

    test_files = partition_test_data(test_file, process_count)
    output_paths = ["tmp/out_{0}.csv".format(i) for i in range(0, process_count)]

    if pickled_classifier_path is None or not os.path.isfile(pickled_classifier_path):
        classifier = __import__(classifier_module).Classifier()
        print "reading training data"
        training = Orange.data.Table(training_file)
        print "read {0} training records".format(len(training))
        classifier.train(training)
        print "training complete"

        pickled_classifier_path = "classifier.pickle"
        cPickle.dump(classifier, open(pickled_classifier_path,'wb'))
        print "pickled"
    else:
        print "using pickled classifier: " + pickled_classifier_path

    console_lock = multiprocessing.Lock()

    '''
    for i in range(0, process_count):
        run(test_files[i], output_paths[i], console_lock)

    '''
    processes = []

    for i in range(0, process_count):
        args = (test_files[i], output_paths[i], console_lock, pickled_classifier_path)
        process = multiprocessing.Process(target=run, args=args)
        processes.append(process)

    process_print("processes created")
    for i in range(0, process_count):
        processes[i].start()

    process_print("processes running")
    for process in processes:
        process.join()
    #'''
    print "processes complete"

    if os.path.isfile("out.csv"):
        os.remove("out.csv")

    with open("out.csv", "w") as out_file:
        out_file.write('Id,Cover_Type\n')
        for i in range(0, process_count):
            with open(output_paths[i], "r") as in_file:
                out_file.writelines(in_file.readlines()[1:])

    elapsed_time = time.time() - start_time
    print('Elapsed time: {0}s'.format(elapsed_time))

if __name__ == "__main__":
    main()