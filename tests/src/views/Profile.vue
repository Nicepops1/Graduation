<template>
  <div class="profile-page">
    <h1>Привет, {{ username }}!</h1>
    <button class="button is-danger" @click="logout">Выйти из учетной записи</button>
  </div>
</template>

<script>
export default {
  name: 'Profile',
  data() {
    return {
      username: ''
    }
  },
  mounted() {
    // Имя пользователя можно хранить в localStorage после логина
    this.username = localStorage.getItem('username') || 'Пользователь';
  },
  methods: {
    logout() {
      localStorage.removeItem('token');
      localStorage.removeItem('username');
      this.$router.push('/login');
    }
  }
}
</script>
