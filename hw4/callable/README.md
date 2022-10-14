<h3> Sorting given folder with threadings</h3>

Threadings are used in directory iteration and file replacement.
New thread for each directory.
New thread for each file replacement operation with using **RLock** to guarantee that file will be replaced in current thread.