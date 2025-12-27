class TodoAPI {
    constructor(baseURL = 'http://localhost:8080') {
        this.baseURL = baseURL;
    }

    async request(endpoint, options = {}) {
        const url = `${this.baseURL}${endpoint}`;
        const config = {
            headers: {
                'Content-Type': 'application/json',
                ...options.headers
            },
            ...options
        };

        try {
            const response = await fetch(url, config);
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            // 204 No Content인 경우 JSON 파싱하지 않음
            if (response.status === 204) {
                return null;
            }
            
            return await response.json();
        } catch (error) {
            console.error('API request failed:', error);
            throw error;
        }
    }

    async getTodos() {
        return this.request('/todos');
    }

    async createTodo(title) {
        return this.request('/todos', {
            method: 'POST',
            body: JSON.stringify({ title, completed: false })
        });
    }

    async updateTodo(id, data) {
        return this.request(`/todos/${id}`, {
            method: 'PUT',
            body: JSON.stringify(data)
        });
    }

    async deleteTodo(id) {
        return this.request(`/todos/${id}`, {
            method: 'DELETE'
        });
    }

    async toggleTodo(id, completed) {
        return this.updateTodo(id, { completed });
    }
}

const todoAPI = new TodoAPI();