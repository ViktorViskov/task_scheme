let app = new Vue({
    el: "#root",
    // variables
    data: {
        // to auth
        isAuth: false,

        // login
        userLogin: "",
        userPassword: "",

        // tasks list
        tasks: [],

        // create task
        task_title: "",
        task_description: "",
        task_start: "",
        task_stop: "",

        // look task on month, date
        date_tasks: "",

        // total used time 
        total: 0,
    },

    methods: {

        Login: async function () {
            // create form data 
            let formData = new FormData();
            formData.append("login", this.userLogin);
            formData.append("password", this.userPassword);

            // delete user users
            this.userLogin = "";
            this.userPassword = "";

            // request to server
            await fetch('/login', {
                method: "POST",
                body: formData                
            });

            // check for auth
            await this.CheckAuth()

            // logick for load task after login
            if (this.isAuth) {
                this.LoadTasks()
            }
        },

        CheckAuth: async function () {
            await fetch('/is_auth').then(response => response.json()).then(data => this.isAuth = Boolean(data.status));
        },

        LoadTasks: async function () {
            await fetch('/tasks').then(response => response.json()).then(data => this.tasks = data);
            this.TotalTime()
        },

        DayTasks: async function () {
            // create form data 
            let formData = new FormData();
            let parsed_date = new Date(this.date_tasks)
            formData.append("date_start",`${parsed_date.getFullYear()}-${parsed_date.getMonth()+1}-${parsed_date.getDate()}T00:00`);
            formData.append("date_stop",`${parsed_date.getFullYear()}-${parsed_date.getMonth()+1}-${parsed_date.getDate()}T23:59`);

            // create task on server
            await fetch('/date_tasks', {
                method: "POST",
                body: formData                
            }).then(response => response.json()).then(data => this.tasks = data);
            this.TotalTime()
        },

        MonthTasks: async function () {
            // create form data 
            let formData = new FormData();
            let parsed_date_start = new Date(`${this.date_tasks}-01T00:00`)
            let parsed_date_stop = new Date(parsed_date_start.getFullYear(),parsed_date_start.getMonth()+1, 0)

            formData.append("date_start",`${parsed_date_start.getFullYear()}-${parsed_date_start.getMonth()+1}-1T00:00`);
            formData.append("date_stop",`${parsed_date_stop.getFullYear()}-${parsed_date_stop.getMonth()+1}-${parsed_date_stop.getDate()}T23:59`);

            // create task on server
            await fetch('/date_tasks', {
                method: "POST",
                body: formData                
            }).then(response => response.json()).then(data => this.tasks = data);
            this.TotalTime()
        },

        UpdateStopTime: function () {
            this.task_stop = this.task_start
        },

        CreateTask: async function () {
            // create form data 
            let formData = new FormData();
            formData.append("title",this.task_title);
            formData.append("description",this.task_description);
            formData.append("start",this.task_start);
            formData.append("stop",this.task_stop);

            // override values
            this.task_title = "",
            this.task_description = "",
            this.task_start = "",
            this.task_stop = "",

            // create task on server
            await fetch('/create', {
                method: "POST",
                body: formData                
            });

            // update tasks
            this.LoadTasks();
        },

        DeleteTask: async function (id) {
            // create form data 
            let formData = new FormData();
            formData.append("task_id",id);

            // delete on server
            await fetch('/delete', {
                method: "POST",
                body: formData                
            });

            // update tasks
            this.LoadTasks();
        },

        Exit: function () {
            // delete all cookies
            document.cookie = "token=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;"
            this.isAuth = false;
        },

        TotalTime: function () {
            this.total = 0
            let minutes = 0
            for (let i = 0; i < this.tasks.length; i++) {
                const start = new Date(this.tasks[i][3])
                const stop = new Date(this.tasks[i][4])
                const different = stop.getTime() - start.getTime()
                minutes += different > 0 ? different / 1000 / 60: 0;
            }

            this.total = `${Math.floor(minutes / 60)}:${minutes - (Math.floor(minutes / 60) * 60)}`
        }
    },

    // when init
    mounted: async function () {
        // check for user auth
        await this.CheckAuth()

        // if user auth load tasks
        if (this.isAuth) {
            // load tasks
            this.LoadTasks()

            // update current start stop time for create page
            const currentDate = new Date()
            this.task_start = `${currentDate.getFullYear()}-${currentDate.getMonth() + 1}-${currentDate.getDate()}T${currentDate.getHours()}:${currentDate.getMinutes()}`
            this.task_stop = `${currentDate.getFullYear()}-${currentDate.getMonth() + 1}-${currentDate.getDate()}T${currentDate.getHours() + 1 > 23 ? currentDate.getHours() : currentDate.getHours() + 1}:${currentDate.getMinutes()}`
        }
    }


});
