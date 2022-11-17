function fetch3rd(path, method, data, handlers) {
    let options = {
        method: method,
        credentials: 'include',
    };

    if (data !== undefined) {
        options.body = JSON.stringify(data)
        options.headers = {
            'Content-Type': 'application/json',
        };
    }
    
    return fetch(path, options).then((response) => {
        if (response.status == 200) {
            if (200 in handlers) {
                return handlers[200](response);
            } else {
                if ('ok' in handlers) {
                    return handlers.ok(await response.json())
                } else {
                    return await response.json()
                }
            }
        } else {
            if (response.status in handlers) {
                return handlers[response.status](response);
            } else {
                throw Error('Unhandled response ' + response.status);
            }
        }
    })
}

function api_registerUser(nome, email, cpf, telefone, senha) {
    return fetch3rd('/api/ciente/registrar', 'POST', { nome, email, cpf, telefone, senha });

    // return fetch('/api/registrar', {
    //     body: JSON.stringify(dados),
    //     method: 'POST',
    //     credentials: 'include',
    // })
    // .then(
    //     (response) => {
    //         if (response.status == 200) {
    //             return await response.json();
    //         } else {
    //             throw Error('Bad response');
    //         }
    //     },

    //     (reason) => {
    //         throw Error('Server did not respond');
    //     }
    // )
}

function api_loginUser(email, senha) {
    return fetch3rd('/api/cliente/login', 'POST', { email, senha }, {
        ok: (user) => ({ ok: true, user }),
        401: (res) => ({ ok: false, err: 'UNAUTHORIZED' }),
    })

    // return fetch('/api/login', {
    //     body: JSON.stringify(dados),
    //     method: 'POST',
    //     credentials: 'include',
    // })
    // .then(
    //     (response) => {
    //         if (response.status == 200) {
    //             return await res.json()
    //         } else if (response.status == 401) {
    //             return 'UNAUTHORIZED'
    //         } else {
    //             throw Error('Bad response')
    //         }
    //     },

    //     (reason) => {
    //         throw Error('Server did not respond');
    //     }
    // )
}

function api_getUser() {
    return fetch3rd('/api/cliente/', 'GET');

    // return fetch('/api/user/')
    // .then(
    //     (response) => {
    //         if (response.ok) {
    //             return await res.json()
    //         } else {
    //             throw Error('Bad response')
    //         }
    //     },

    //     (reason) => {
    //         throw Error('Server did not response');
    //     }
    // );
}

function api_logoutUser() {
    await fetch3rd('/api/cliente/logout', 'POST', undefined, {
        200: (res) => {}
    });
}

function api_toggleAdmin() {
    await fetch3rd('/api/cliente/toggle-admin', 'POST', undefined, {
        200: (res) => {}
    });
}