tasks = []


def add_task():
    task = input("Enter task: ")
    tasks.append({"task": task, "completed": False})
    print("Task added successfully!")


def view_tasks():
    if not tasks:
        print("No tasks found.")
        return

    print("\n--- TO-DO LIST ---")

    for i, item in enumerate(tasks, start=1):
        status = "Completed" if item["completed"] else "Pending"
        print(f"{i}. {item['task']} - {status}")


def complete_task():
    view_tasks()

    if tasks:
        number = int(input("Enter task number to complete: "))

        if 1 <= number <= len(tasks):
            tasks[number - 1]["completed"] = True
            print("Task completed successfully!")
        else:
            print("Invalid task number.")


def delete_task():
    view_tasks()

    if tasks:
        number = int(input("Enter task number to delete: "))

        if 1 <= number <= len(tasks):
            tasks.pop(number - 1)
            print("Task deleted successfully!")
        else:
            print("Invalid task number.")


while True:
    print("\n===== TO-DO LIST =====")
    print("1. Add Task")
    print("2. View Tasks")
    print("3. Complete Task")
    print("4. Delete Task")
    print("5. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        add_task()

    elif choice == "2":
        view_tasks()

    elif choice == "3":
        complete_task()

    elif choice == "4":
        delete_task()

    elif choice == "5":
        print("Thank you!")
        break

    else:
        print("Invalid choice. Please try again.")