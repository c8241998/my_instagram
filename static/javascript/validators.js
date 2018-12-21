var email_regex = new RegExp("^[a-z0-9]+([._\\\\-]*[a-z0-9])*@([a-z0-9]+[-a-z0-9]*[a-z0-9]+.){1,63}[a-z0-9]+$");
var username_regex = new RegExp("^([a-z0-9\-_])+$");
var website_regex = /^(?=^.{3,255}$)(http(s)?:\/\/)?(www\.)?[a-zA-Z0-9][-a-zA-Z0-9]{0,62}(\.[a-zA-Z0-9][-a-zA-Z0-9]{0,62})+(:\d+)*(\/\w+\.\w+)*$/;
var phone_regex = /^1(?:3\d|4[4-9]|5[0-35-9]|6[67]|7[013-8]|8\d|9\d)\d{8}$/;

var validateUsernameEmail = (rule, value, callback) => {
    if (!username_regex.test(value) && !email_regex.test(value)) {
        callback(new Error('please check your username or email address.'));
    } else {
        callback();
    }
};

var validateUsername = (rule, value, callback) => {
    if (!username_regex.test(value)) {
        callback(new Error('please check your username.'));
    }
    else {
        callback();
    }
};

var validateEmail = (rule, value, callback) => {
    if (!email_regex.test(value)) {
        callback(new Error('please check your email address.'));
    } else {
        callback();
    }
};

var validateWebsite = (rule, value, callback) => {
    if (!website_regex.test(value)) {
        callback(new Error('invalid website.'));
    } else {
        callback();
    }
};

var validateDescription = (rule, value, callback) => {
    if (value.length > 40) {
        callback(new Error('40 characters at most.'));
    } else {
        callback();
    }
};

var validatePhone = (rule, value, callback) => {
    if (!phone_regex.test(value)) {
        callback(new Error('invalid phone number.'));
    } else {
        callback();
    }
};

var validateSex = (rule, value, callback) => {
    if (value !== 'male' && value !== 'female' && value !== 'unknown') {
        callback(new Error('invalid sex.'));
    } else {
        callback();
    }
};
