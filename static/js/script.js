document.addEventListener('DOMContentLoaded', function() {
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.startsWith(name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    const csrftoken = getCookie('csrftoken');

    document.querySelectorAll('.add-to-favorites').forEach(button => {
        button.addEventListener('click', function(event) {
            event.preventDefault();
            const productId = this.dataset.productId;
            const url = `/favorites/add/${productId}/`;

            fetch(url, {
                method: 'GET',
                headers: {
                    'X-CSRFToken': csrftoken,
                    'Content-Type': 'application/json',
                },
            })
            .then(response => response.json())
            .then(data => {
                if (data.favorites_count !== undefined) {
                    document.getElementById('favorites-count').textContent = data.favorites_count;
                }
            })
            .catch(error => {
                console.error('Ошибка при добавлении в избранное:', error);
            });
        });
    });

    document.querySelectorAll('.add-to-basket').forEach(button => {
        button.addEventListener('click', function(event) {
            event.preventDefault();
            const productId = this.dataset.productId;
            const url = `/basket/add/${productId}/`;

            fetch(url, {
                method: 'GET',
                headers: {
                    'X-CSRFToken': csrftoken,
                    'Content-Type': 'application/json',
                },
            })
            .then(response => response.json())
            .then(data => {
                if (data.basket_count !== undefined) {
                    document.getElementById('basket-count').textContent = data.basket_count;
                }
            })
            .catch(error => {
                console.error('Ошибка при добавлении в корзину:', error);
            });
        });
    });

    fetch('/get_counts/', {
        method: 'GET',
        headers: {
            'X-CSRFToken': csrftoken,
            'Content-Type': 'application/json',
        },
    })
    .then(response => response.json())
    .then(data => {
        if (data.favorites_count !== undefined) {
            document.getElementById('favorites-count').textContent = data.favorites_count;
        }
        if (data.basket_count !== undefined) {
            document.getElementById('basket-count').textContent = data.basket_count;
        }
    })
    .catch(error => {
        console.error('Ошибка при получении количества товаров:', error);
    });
});
