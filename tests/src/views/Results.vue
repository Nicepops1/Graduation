<template>
  <div class="results-page">
    <h1>Результаты</h1>
    <section>
      <h2>Тесты, которые вы прошли</h2>
      <ul>
        <li v-for="result in userResults" :key="result.id">
          {{ result.test_name }} — {{ result.score }} баллов
        </li>
      </ul>
      <div v-if="userResults.length === 0">Нет пройденных тестов.</div>
    </section>
    <section>
      <h2>Результаты пользователей по вашим тестам</h2>
      <ul>
        <li v-for="result in createdTestResults" :key="result.id">
          {{ result.username }} — {{ result.test_name }} — {{ result.score }} баллов
        </li>
      </ul>
      <div v-if="createdTestResults.length === 0">Нет результатов по вашим тестам.</div>
    </section>
  </div>
</template>

<script>
import axios from 'axios';
export default {
  name: 'Results',
  data() {
    return {
      userResults: [],
      createdTestResults: []
    }
  },
  mounted() {
    const token = localStorage.getItem('jwt_token');
    axios.get('http://127.0.0.1:8000/api/v1/user/tests/results/', {
      headers: { Authorization: `Token ${token}` }
    })
      .then(res => {
        this.userResults = res.data;
      })
      .catch(() => {
        this.userResults = [];
      });
    axios.get('http://127.0.0.1:8000/api/v1/user/created-tests/results/', {
      headers: { Authorization: `Token ${token}` }
    })
      .then(res => {
        this.createdTestResults = res.data;
      })
      .catch(() => {
        this.createdTestResults = [];
      });
  }
}
</script>
