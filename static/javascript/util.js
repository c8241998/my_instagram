function jump(url) {
    window.location.href = url;
}

function post(vue, url) {
    vue.$refs.form.validate((valid) => {
        if (valid) {
            var form = document.createElement("form");
            form.action = url;
            form.method = "post";
            form.style.display = "none";

            for (var param in vue.data) {
                var opt = document.createElement("textarea");
                opt.name = param;
                opt.value = vue.data[param];
                form.appendChild(opt);
            }

            document.body.appendChild(form);
            form.submit();
        } else return false;
    });
}