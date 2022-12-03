function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
  }

function fetch3rd(path, method, data, handlers) {
    let options = {
        method: method,
        credentials: 'include',
        headers: {
            'X-CSRF-TOKEN': getCookie('csrf_access_token')
        },
    };

    // let token = sessionStorage.getItem('auth_token')
    // if (token !== null) {
    //     options.headers['Authorization'] = 'Bearer ' + token;
    // }

    if (handlers == undefined) {
        handlers = {}
    }

    if (data !== undefined) {
        options.body = JSON.stringify(data)
        options.headers['Content-Type'] = 'application/json';
    }
    
    return fetch(path, options).then(async (response) => {

        // if (response.headers.has('X-new-authorization')) {
        //     sessionStorage.setItem('auth_token', response.headers.get('X-new-authorization'))
        // }

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
    return fetch3rd('/api/cliente/registrar', 'POST', { nome, email, cpf, telefone, senha });
}

function api_loginUser(email, senha) {
    return fetch3rd('/api/cliente/login', 'POST', { email, senha }, {
        ok: (user) => ({ ok: true, user }),
        404: (res) => ({ ok: false, err: 'not_found'}),
        401: (res) => ({ ok: false, err: 'unauthorized' }),
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

function api_novoImovel(nome, descricao, cidade, bairro, area, quartos, apartamento, quintal) {
    return fetch3rd(
        '/api/imovel/',
        'POST',
        { nome, descricao, cidade, bairro, area, quartos, apartamento, quintal}
    )
}