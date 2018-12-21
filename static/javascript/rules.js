function required_rule(message) {
    return {required: true, message: message, trigger: ['blur', 'change']};
}

function validator_rule(validator) {
    return {validator:validator , trigger: ['blur', 'change']};
}

function min_rule(len,message) {
    return {min: len, message: message, trigger: ['blur', 'change']};
}