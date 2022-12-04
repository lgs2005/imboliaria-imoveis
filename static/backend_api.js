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

    if (handlers == undefined) {
        handlers = {}
    }

    if (data !== undefined) {
        if (method === 'GET') {
            path = path + '?' + new URLSearchParams(data);
        } else {
            options.body = JSON.stringify(data)
            options.headers['Content-Type'] = 'application/json';
        }
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

function api_novoImovel(dados) {
    return fetch3rd(
        '/api/imovel/',
        'POST',
        dados
    )
}

function api_alterarImovel(id, dados) {
    return fetch3rd(
        '/api/imovel/' + id,
        'PATCH',
        dados,
    )
}

function api_busca(pagina, dados) {
    return fetch3rd(
        '/api/busca/',
        'GET',
        {...dados, page: pagina}
    )
}

function api_adicionarVenda(imovel, tipo, preco) {
    return fetch3rd(
        '/api/venda/' + imovel,
        'POST',
        { tipo, preco }
    )
}

function api_comprarImovel(imovel) {
    return fetch3rd(
        '/api/venda/' + imovel + '/comprar',
        'POST'
    )
}