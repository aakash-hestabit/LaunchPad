const main = document.getElementsByTagName("main")[0];
let tasks = JSON.parse(window.localStorage.getItem("tasks") || "[]");

const add_btn = document.getElementsByClassName("add_btn")[0];

function appendTask(task) {
    const noTasksMsg = document.querySelector(".no_tasks");
    if (noTasksMsg) noTasksMsg.remove();

    const t = document.createElement("article");
    t.classList.add("task");

    const checkbox = document.createElement("input");
    checkbox.type = "checkbox";
    checkbox.checked = task.completed;
    checkbox.classList.add("checkbox");
    checkbox.addEventListener("change", (e) => {
        task.completed = e.currentTarget.checked;
        window.localStorage.setItem("tasks", JSON.stringify(tasks));
        desc.classList.toggle("completed", task.completed);
    });

    const desc = document.createElement("p");
    desc.classList.add("desc");
    task.completed && desc.classList.add("completed");
    desc.innerHTML = task.desc;

    const edit_btn = document.createElement("button");
    edit_btn.classList.add("edit_btn", "btn");
    edit_btn.innerHTML = "🖋";
    edit_btn.addEventListener("click", async() => {
        const newDesc = await editTask(task.desc);
        if (newDesc) {
            task.desc = newDesc;
            desc.innerHTML = newDesc;
            window.localStorage.setItem("tasks", JSON.stringify(tasks));
        }
    });

    const delete_btn = document.createElement("button");
    delete_btn.classList.add("delete_btn", "btn");
    delete_btn.innerHTML = "❌";
    delete_btn.addEventListener("click", () => {
        tasks = tasks.filter(tk => tk.id !== task.id);
        window.localStorage.setItem("tasks", JSON.stringify(tasks));
        t.remove();

        if (tasks.length === 0) {
            const p = document.createElement('p');
            p.innerHTML = "NO TASKS YET";
            p.classList.add("no_tasks");
            main.appendChild(p);
        }
    });

    t.appendChild(checkbox);
    t.appendChild(desc);
    t.appendChild(edit_btn);
    t.appendChild(delete_btn);
    main.appendChild(t);
}

add_btn.addEventListener("click", async() => {
    const desc = await editTask("");
    if (!desc) return;

    const newTask = {
        id: Date.now(),
        desc,
        completed: false
    };
    tasks.push(newTask);
    window.localStorage.setItem("tasks", JSON.stringify(tasks));

    appendTask(newTask);
});

if (tasks.length === 0) {
    const p = document.createElement('p');
    p.innerHTML = "NO TASKS YET";
    p.classList.add("no_tasks");
    main.appendChild(p);
} else {
    tasks.forEach(task => appendTask(task));
}

function editTask(initial) {
    return new Promise((resolve) => {
        const overlay = document.createElement("div");
        overlay.classList.add("overlay");

        const popup = document.createElement("section");
        popup.classList.add("popup");

        const form = document.createElement("form");
        form.classList.add("popup_form");

        const label = document.createElement("label");
        label.classList.add("popup_label");
        label.innerText = "Task";

        const input = document.createElement("input");
        input.type = "text";
        input.value = initial || "";
        input.placeholder = "Enter task...";
        input.classList.add("popup_input");

        const submit = document.createElement("button");
        submit.type = "submit";
        submit.innerText = "Save";
        submit.classList.add("popup_submit");

        form.appendChild(label);
        form.appendChild(input);
        form.appendChild(submit);
        popup.appendChild(form);
        overlay.appendChild(popup);
        document.body.appendChild(overlay);
        input.focus();

        form.addEventListener("submit", (e) => {
            e.preventDefault();
            const val = input.value.trim();
            if (val) {
                document.body.removeChild(overlay);
                resolve(val);
            } else {
                alert("Task cannot be empty!");
            }
        });

        overlay.addEventListener("click", (e) => {
            if (e.target === overlay) {
                document.body.removeChild(overlay);
                resolve(null);
            }
        });
    });
}