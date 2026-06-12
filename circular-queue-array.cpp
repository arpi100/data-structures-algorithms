#include <iostream>
using namespace std;

#define MAX 5  // Using a macro for size

int queue_arr[MAX];
int head = -1;
int tail = -1;

// Function to add data
void addElement(int item) {
    // Check if full
    if ((tail + 1) % MAX == head) {
        cout << "Queue is Full!" << endl;
        return;
    }

    if (head == -1) head = 0; // First element case

    tail = (tail + 1) % MAX;
    queue_arr[tail] = item;
    cout << "Inserted: " << item << endl;
}

// Function to remove data
void removeElement() {
    if (head == -1) {
        cout << "Queue is Empty!" << endl;
        return;
    }

    int deleted = queue_arr[head];
    
    if (head == tail) {
        // Reset if it was the last element
        head = -1;
        tail = -1;
    } else {
        head = (head + 1) % MAX;
    }
    cout << "Removed: " << deleted << endl;
}

// Function to show the queue
void showQueue() {
    if (head == -1) {
        cout << "Nothing to show." << endl;
        return;
    }

    cout << "Current Queue: ";
    int index = head;
    while (true) {
        cout << queue_arr[index] << " ";
        if (index == tail) break;
        index = (index + 1) % MAX;
    }
    cout << endl;
}

int main() {
    // Fill the queue
    addElement(10);
    addElement(20);
    addElement(30);
    addElement(40);
    addElement(50);
    addElement(60); // Full

    // Empty the queue
    removeElement();
    removeElement();
    removeElement();
    removeElement();
    removeElement();
    removeElement(); // Empty

    showQueue();

    return 0;
}