class TodoApp {
    constructor() {
        this.todos = [];
        this.initializeElements();
        this.attachEventListeners();
        this.loadTodos();
    }

    initializeElements() {
        this.todoForm = document.getElementById('addTodoForm');
        this.todoInput = document.getElementById('todoInput');
        this.todoList = document.getElementById('todoList');
        this.totalCount = document.getElementById('totalCount');
        this.completedCount = document.getElementById('completedCount');
        this.pendingCount = document.getElementById('pendingCount');
    }

    attachEventListeners() {
        this.todoForm.addEventListener('submit', (e) => this.handleAddTodo(e));
    }

    async loadTodos() {
        try {
            this.showLoading();
            this.todos = await todoAPI.getTodos();
            this.renderTodos();
            this.updateStats();
        } catch (error) {
            this.showError('투두 목록을 불러오는데 실패했습니다.');
            console.error('Failed to load todos:', error);
        }
    }

    async handleAddTodo(e) {
        e.preventDefault();
        const title = this.todoInput.value.trim();
        
        if (!title) return;

        try {
            const newTodo = await todoAPI.createTodo(title);
            this.todos.push(newTodo);
            this.todoInput.value = '';
            this.renderTodos();
            this.updateStats();
        } catch (error) {
            this.showError('투두 추가에 실패했습니다.');
            console.error('Failed to add todo:', error);
        }
    }

    async handleToggleTodo(id) {
        try {
            const todo = this.todos.find(t => t.id === id);
            if (!todo) return;

            const updatedTodo = await todoAPI.toggleTodo(id, !todo.completed);
            const index = this.todos.findIndex(t => t.id === id);
            this.todos[index] = updatedTodo;
            
            this.renderTodos();
            this.updateStats();
        } catch (error) {
            this.showError('투두 상태 변경에 실패했습니다.');
            console.error('Failed to toggle todo:', error);
        }
    }

    async handleDeleteTodo(id) {
        if (!confirm('정말 삭제하시겠습니까?')) return;

        try {
            await todoAPI.deleteTodo(id);
            this.todos = this.todos.filter(t => t.id !== id);
            console.log(id);
            console.log(this.todos);

            this.renderTodos();
            this.updateStats();
        } catch (error) {
            this.showError('투두 삭제에 실패했습니다.');
            console.error('Failed to delete todo:', error);
        }
    }

    async handleEditTodo(id) {
        const todo = this.todos.find(t => t.id === id);
        if (!todo) return;

        const newTitle = prompt('새로운 제목을 입력하세요:', todo.title);
        if (!newTitle || newTitle.trim() === todo.title) return;

        try {
            const updatedTodo = await todoAPI.updateTodo(id, { title: newTitle.trim() });
            const index = this.todos.findIndex(t => t.id === id);
            this.todos[index] = updatedTodo;
            
            this.renderTodos();
        } catch (error) {
            this.showError('투두 수정에 실패했습니다.');
            console.error('Failed to edit todo:', error);
        }
    }

    renderTodos() {
        this.todoList.innerHTML = '';

        if (this.todos.length === 0) {
            this.todoList.innerHTML = '<li class="loading">투두가 없습니다. 새로운 투두를 추가해보세요!</li>';
            return;
        }

        this.todos.forEach(todo => {
            const li = document.createElement('li');
            li.className = `todo-item ${todo.completed ? 'completed' : ''}`;
            
            li.innerHTML = `
                <input type="checkbox" 
                       class="todo-checkbox" 
                       ${todo.completed ? 'checked' : ''}
                       onchange="app.handleToggleTodo(${todo.id})">
                <span class="todo-text">${this.escapeHtml(todo.title)}</span>
                <div class="todo-actions">
                    <button class="btn btn-edit" onclick="app.handleEditTodo(${todo.id})">수정</button>
                    <button class="btn btn-delete" onclick="app.handleDeleteTodo(${todo.id})">삭제</button>
                </div>
            `;
            
            this.todoList.appendChild(li);
        });
    }

    updateStats() {
        const total = this.todos.length;
        const completed = this.todos.filter(t => t.completed).length;
        const pending = total - completed;

        this.totalCount.textContent = `전체: ${total}`;
        this.completedCount.textContent = `완료: ${completed}`;
        this.pendingCount.textContent = `남은 것: ${pending}`;
    }

    showLoading() {
        this.todoList.innerHTML = '<li class="loading">로딩 중...</li>';
    }

    showError(message) {
        const errorDiv = document.createElement('div');
        errorDiv.className = 'error';
        errorDiv.textContent = message;
        
        // 기존 에러 메시지 제거
        const existingError = document.querySelector('.error');
        if (existingError) {
            existingError.remove();
        }
        
        // 에러 메시지를 폼 위에 추가
        this.todoForm.parentNode.insertBefore(errorDiv, this.todoForm);
        
        // 5초 후 자동 제거
        setTimeout(() => {
            errorDiv.remove();
        }, 5000);
    }

    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
}

// 앱 초기화
document.addEventListener('DOMContentLoaded', () => {
    window.app = new TodoApp();
});