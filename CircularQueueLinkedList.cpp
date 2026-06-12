#include <iostream>
using namespace std;

// Using a constructor inside the struct to make node creation cleaner
struct Node {
    int value;
    Node* next;
    
    Node(int val) {
        value = val;
        next = NULL;
    }
};

class MyCircularQueue {
private:
    Node* head;
    Node* tail;

public:
    MyCircularQueue() {
        head = NULL;
        tail = NULL;
    }

    bool isQueueEmpty() {
        return (head == NULL);
    }

    void insert(int data) {
        Node* entry = new Node(data);

        if (isQueueEmpty()) {
            head = tail = entry;
            tail->next = head; // Pointing back to make it circular
        } else {
            tail->next = entry;
            tail = entry;
            tail->next = head; // Maintenance of circular link
        }
        cout << "Inserted: " << data << endl;
    }

    void remove() {
        if (isQueueEmpty()) {
            cout << "Queue is already empty!" << endl;
            return;
        }

        int removedVal;
        if (head == tail) {
            // Case: Single element remaining
            removedVal = head->value;
            delete head;
            head = tail = NULL;
        } else {
            Node* temp = head;
            removedVal = head->value;
            head = head->next;
            tail->next = head; // Connect last node to new head
            delete temp;
        }
        cout << "Removed: " << removedVal << endl;
    }

    void printAll() {
        if (isQueueEmpty()) {
            cout << "Nothing to display." << endl;
            return;
        }

        Node* current = head;
        cout << "Queue items: ";
        // Standard loop logic to avoid 'do-while' for variety
        while (true) {
            cout << current->value << " ";
            current = current->next;
            if (current == head) break;
        }
        cout << endl;
    }
};

int main() {
    MyCircularQueue q;

    q.insert(29);
    q.insert(15);
    q.insert(10);
    q.insert(12);
    q.insert(35);
    q.insert(40);
    q.printAll();

    q.remove();
    q.remove();
    q.remove();
    q.printAll();

    q.remove();
    q.remove();
    q.remove();
    q.remove(); // Test empty case
    q.printAll();

    return 0;
}