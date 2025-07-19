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
                        <input type="text" class="input" v-model="password">
                    </div>
                </div>
                <div class="notification is-danger" v-if="errors.length">
                    <p v-for="error in errors" v-bind:key="error">{{ error }}</p>
                </div>
                <div class="field">
                    <div class="control">
                        <button class="button is-white">Войти</button>
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
}
</script>