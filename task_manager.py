import json
import os
from datetime import datetime

DATA_FILE = "tasks.json"


# ---------------- File Handling ----------------
def load_tasks():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_tasks(tasks):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(tasks, f, indent=4, ensure_ascii=False)


# ---------------- Utilities ----------------
def generate_id(tasks):
    if not tasks:
        return 1
    return max(task["id"] for task in tasks) + 1


def valid_date(date_str):
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False


# ---------------- Core Features ----------------
def add_task(tasks):
    title = input("ชื่องาน: ").strip()
    if not title:
        print(" ชื่องานห้ามว่าง")
        return

    description = input("คำอธิบาย: ").strip()
    due_date = input("วันครบกำหนด (YYYY-MM-DD): ").strip()

    if not valid_date(due_date):
        print(" รูปแบบวันที่ไม่ถูกต้อง")
        return

    task = {
        "id": generate_id(tasks),
        "title": title,
        "description": description,
        "due_date": due_date,
        "completed": False
    }

    tasks.append(task)
    save_tasks(tasks)
    print(" เพิ่มงานเรียบร้อย")


def view_tasks(tasks):
    tasks_sorted = sorted(tasks, key=lambda x: x["due_date"])

    pending = [t for t in tasks_sorted if not t["completed"]]
    completed = [t for t in tasks_sorted if t["completed"]]

    print("\n งานรอดำเนินการ")
    for t in pending:
        print(f"[{t['id']}] {t['title']} (ครบกำหนด: {t['due_date']})")

    print("\n งานที่เสร็จแล้ว")
    for t in completed:
        print(f"[{t['id']}] {t['title']}")


def mark_complete(tasks):
    try:
        task_id = int(input("ใส่ ID งานที่เสร็จแล้ว: "))
    except ValueError:
        print(" ID ต้องเป็นตัวเลข")
        return

    for task in tasks:
        if task["id"] == task_id:
            task["completed"] = True
            save_tasks(tasks)
            print(" ทำเครื่องหมายเสร็จสิ้นแล้ว")
            return

    print(" ไม่พบงาน")


def delete_task(tasks):
    try:
        task_id = int(input("ใส่ ID งานที่ต้องการลบ: "))
    except ValueError:
        print(" ID ต้องเป็นตัวเลข")
        return

    for task in tasks:
        if task["id"] == task_id:
            tasks.remove(task)
            save_tasks(tasks)
            print(" ลบงานเรียบร้อย")
            return

    print(" ไม่พบงาน")


def search_tasks(tasks):
    keyword = input("ค้นหาด้วยคำหรือวันที่ (YYYY-MM-DD): ").lower()

    results = [
        t for t in tasks
        if keyword in t["title"].lower()
        or keyword in t["description"].lower()
        or keyword == t["due_date"]
    ]

    if not results:
        print(" ไม่พบงานที่ค้นหา")
        return

    for t in results:
        status = "✔" if t["completed"] else " "
        print(f"[{t['id']}] {t['title']} {status}")


# ---------------- CLI Menu ----------------
def menu():
    print("""
========= Python Task Manager =========
1. เพิ่มงานใหม่
2. ดูงานทั้งหมด
3. ทำเครื่องหมายว่างานเสร็จสิ้น
4. ลบงาน
5. ค้นหางาน
6. ออกจากโปรแกรม
""")


def main():
    tasks = load_tasks()

    while True:
        menu()
        choice = input("เลือกเมนู (1-6): ").strip()

        if choice == "1":
            add_task(tasks)
        elif choice == "2":
            view_tasks(tasks)
        elif choice == "3":
            mark_complete(tasks)
        elif choice == "4":
            delete_task(tasks)
        elif choice == "5":
            search_tasks(tasks)
        elif choice == "6":
            print(" ออกจากโปรแกรม")
            break
        else:
            print(" กรุณาเลือกเมนูที่ถูกต้อง")


if __name__ == "__main__":
    main()






