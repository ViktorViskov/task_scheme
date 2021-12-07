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
    },

    methods: {

        Login: async function (userLogin, userPassword) {

            // create form data 
            let formData = new FormData();
            formData.append("login",userLogin);
            formData.append("password",userPassword);

            // request to server
            await fetch('/login', {
                method: "POST",
                body: formData                
            });

            // check for auth
            this.CheckAuth()
        },

        CheckAuth: async function () {
            await fetch('/is_auth').then(response => response.json()).then(data => this.isAuth = Boolean(data.status));
        },

        LoadTasks: async function () {
            await fetch('/tasks').then(response => response.json()).then(data => this.tasks = data);
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
        }
    },

    // when init
    mounted: async function () {
        // check for user auth
        await this.CheckAuth()

        // if user auth load tasks
        if (this.isAuth) {
            this.LoadTasks()
        }
    }


});