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
    
    return fetch(path, options).then(async (response) => {
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
}

function api_loginUser(email, senha) {
    return fetch3rd('/api/cliente/login', 'POST', { email, senha }, {
        ok: (user) => ({ ok: true, user }),
        401: (res) => ({ ok: false, err: 'UNAUTHORIZED' }),
    })
}

function api_getUser() {
    return fetch3rd('/api/cliente/', 'GET');
}

async function api_logoutUser() {
    await fetch3rd('/api/cliente/logout', 'POST', undefined, {
        200: (res) => {}
    });
}

async function api_toggleAdmin() {
    await fetch3rd('/api/cliente/toggle-admin', 'POST', undefined, {
        200: (res) => {}
    });
}
