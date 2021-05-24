import os
import errno

OUTPUT_FOLDER = "data"

def write_data(data, folder, file_name):
    filename = "./data/" + folder + "/" + file_name;
    if not os.path.exists(os.path.dirname(filename)):
        try:
            os.makedirs(os.path.dirname(filename))
        except OSError as exc: # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise

    with open(filename, "w") as f:
        f.write(data)
