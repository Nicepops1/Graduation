<template>
    <div class="page-sign-up">
        <div class="columns">
            <div class="column is-4 is-offset-4">
            <h1 class="title">Регистрация</h1>

            <form @submit.prevent="submitForm">
                <div class="field">
                    <label>Имя пользователя</label>
                    <div class="control">
                        <input type="text" class="input" v-model="username">
                    </div>
                </div>
                <div class="field">
                    <label>Электронная почта</label>
                    <div class="control">
                        <input type="text" class="input" v-model="email">
                    </div>
                </div>
                <div class="field">
                    <label>Пароль</label>
                    <div class="control">
                        <input type="password" class="input" v-model="password">
                    </div>
                </div>
                <div class="field">
                    <label>Подтвердите пароль</label>
                    <div class="control">
                        <input type="password" class="input" v-model="password2">
                    </div>
                </div>
                <div class="notification is-danger" v-if="errors.length">
                    <p v-for="error in errors" v-bind:key="error">{{ error }}</p>
                </div>
                <div class="field">
                    <div class="control">
                        <button class="button is-dark">Зарегистрироваться</button>
                    </div>
                </div>
                <hr>
                Или вы можете нажать <router-link to="/log-in">сюда</router-link> чтобы войти в аккаунт!
            </form>
        </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios';
import { toast } from 'bulma-toast'
export default {
    name: 'SignUp',
    data() {
        return {
        username: '',
        email: '',
        password: '',
        password2: '',
        errors: []
        }
    },
    methods: {
        submitForm() {
            this.errors = []

            if (this.username === '') {
                this.errors.push('Не введено имя пользователя')
            }

            if (this.password.length <= 8) {
                this.errors.push('Пароль слишком короткий')
            }
            if (this.password !== this.password2) {
                this.errors.push('Пароли не совпадают')
            }
            
            if (!this.errors.length) {
                const formData = {
                    headers: {
                                CORS : 'Access-Control-Allow-Origin',
                            },
                    username: this.username,
                    password: this.password,
                    email: this.email
                }

                axios
                    .post('http://127.0.0.1:8000/api/v1/users/', formData)
                    .then(response => {

                        toast({
                            message: 'Учетная запись создана, входите!',
                            type: 'is-succesful',
                            dismissable: true,
                            pauseOnHover: true,
                            duration: 2000,
                            position: 'bottom-right',
                        })
                        this.$router.push('/login')
                    })
                    .catch(error => {
                        if (error.response) {
                            for (const property in error.response.data) {
                                this.errors.push(`${property}: ${error.response.data[property]}`)
                            }
                            console.log(JSON.stringify(error.response.data))
                        } else if (error.message) {
                            this.errors.push('Что-то пошло не так. Попробуйте снова')
                            console.log(error.message)
                        }
                    })
            }

        }
    }
}
</script>