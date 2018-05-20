class Formulario {

    constructor(nome, email, texto) {

        this._nome = nome
        this._email = email;
        this._texto = texto;
        Object.freeze(this);
    }

    get nome() {

        return this._nome;
    }

    get email() {

        return this._email;
    }

    get texto() {

        return this._texto;
    }
}