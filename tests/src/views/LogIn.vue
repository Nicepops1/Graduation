<template>
    <div class="page-log-in">
        <div class="columns">
            <div class="column is-4 is-offset-4">
            <h1 class="title">Вход в аккаунт</h1>

            <form @submit.prevent="submitForm">
                <div class="field">
                    <label>Имя пользователя</label>
                    <div class="control">
                        <input type="text" class="input" v-model="username">
                    </div>
                </div>
                <div class="field">
                    <label>Пароль</label>
                    <div class="control">
                        <input type="password" class="input" v-model="password">
                    </div>
                </div>
                <div class="notification is-danger" v-if="errors.length">
                    <p v-for="error in errors" v-bind:key="error">{{ error }}</p>
                </div>
                <div class="field">
                    <div class="control">
                        <button class="button is-dark">Войти</button>
                    </div>
                </div>
                <hr>
                Или вы можете нажать <router-link to="/signup">сюда</router-link> чтобы зарегистрироваться!
            </form>
        </div>
        </div>
    </div>

</template>
<script>
import axios from 'axios';
import { toast } from 'bulma-toast'
export default {
    name: 'LogIn',
    data() {
        return {
        username: '',
        password: '',
        errors: []
        }
    },
    mounted() {
        if (this.$route.query.redirected) {
            toast({
                message: 'Вы были перенаправлены на страницу входа, так как не авторизованы.',
                type: 'is-info',
                dismissable: true,
                pauseOnHover: true,
                duration: 3000,
                position: 'bottom-right',
            });
        }
    },
    methods: {
        submitForm() {
            this.errors = [];
            if (this.username === '') {
                this.errors.push('Не введено имя пользователя');
            }
            if (this.password.length <= 8) {
                this.errors.push('Пароль слишком короткий');
            }
            if (!this.errors.length) {
                const formData = {
                    username: this.username,
                    password: this.password
                };
                axios
                    .post('http://127.0.0.1:8000/api/v1/token/login/', formData)
                    .then(response => {
                        // Если сервер возвращает токен, сохраняем его
                        if (response.data && response.data.auth_token) {
                            localStorage.setItem('token', response.data.auth_token);
                            localStorage.setItem('username', this.username);
                            console.log(response.data.auth_token)
                        }
                        toast({
                            message: 'Вход выполнен успешно!',
                            type: 'is-success',
                            dismissable: true,
                            pauseOnHover: true,
                            duration: 2000,
                            position: 'bottom-right',
                        });
                        this.$router.push('/profile');
                    })
                    .catch(error => {
                        if (error.response) {
                            for (const property in error.response.data) {
                                this.errors.push(`${property}: ${error.response.data[property]}`);
                            }
                            console.log(JSON.stringify(error.response.data));
                        } else if (error.message) {
                            this.errors.push('Что-то пошло не так. Попробуйте снова');
                            console.log(error.message);
                        }
                    });
            }
        }
    }
}
</script>