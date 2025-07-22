<template>
  <div class="results-page">
    <h1>Результаты</h1>
    <section>
      <h2>Тесты, которые вы прошли</h2>
      <ul>
        <li v-for="result in userResults" :key="result.id">
          {{ result.test_name }} — {{ result.score }} баллов — <span style="color: #888">{{ formatDate(result.completed_at) }}</span>
        </li>
      </ul>
      <div v-if="userResults.length === 0">Нет пройденных тестов.</div>
    </section>
    <section>
      <h2>Результаты пользователей по вашим тестам</h2>
      <div v-if="createdTestResults.length">
        <div class="field">
          <label class="label">Выберите тест</label>
          <div class="control">
            <div class="select">
              <select v-model="selectedTestId" @change="fetchDetailedResults">
                <option disabled value="">-- Выберите тест --</option>
                <option v-for="test in createdTests" :key="test.test_id" :value="test.test_id">{{ test.title }}</option>
              </select>
            </div>
          </div>
        </div>
        <div v-if="detailedResults">
          <button class="button is-info mb-2" @click="exportToCSV">Экспорт в CSV</button>
          <div style="overflow-x: auto; overflow-y: auto; max-height: 500px;">
            <table class="table is-bordered is-striped is-narrow is-hoverable is-fullwidth">
              <thead>
                <tr>
                  <th>Пользователь</th>
                  <th v-for="(q, idx) in detailedResults.questions" :key="idx">{{ q }}</th>
                  <th>Баллы</th>
                  <th>Дата прохождения</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="user in detailedResults.results" :key="user.username + user.completed_at">
                  <td>{{ user.username }}</td>
                  <td v-for="ans in user.answers" :key="ans.question" :class="ans.is_correct ? 'has-background-success-light' : 'has-background-danger-light'">
                    <span v-if="ans.is_correct">✔</span>
                    <span v-else>✘</span>
                    <span v-if="ans.user_answer"> ({{ ans.user_answer }})</span>
                  </td>
                  <td><b>{{ user.score }}</b></td>
                  <td>{{ formatDate(user.completed_at) }}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
      <div v-else>Нет результатов по вашим тестам.</div>
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
      createdTestResults: [],
      createdTests: [],
      selectedTestId: '',
      detailedResults: null
    }
  },
  mounted() {
    const token = localStorage.getItem('token');
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
        // Собираем уникальные тесты для выбора
        const testMap = {};
        res.data.forEach(r => {
          if (!testMap[r.test_id]) {
            testMap[r.test_id] = { test_id: r.test_id, title: r.test_name };
          }
        });
        this.createdTests = Object.values(testMap);
      })
      .catch(() => {
        this.createdTestResults = [];
      });
  },
  methods: {
    formatDate(dt) {
      if (!dt) return '';
      const d = new Date(dt);
      return d.toLocaleString();
    },
    async fetchDetailedResults() {
      this.detailedResults = null;
      if (!this.selectedTestId) return;
      const token = localStorage.getItem('token');
      try {
        const res = await axios.get(`http://127.0.0.1:8000/api/v1/tests/${this.selectedTestId}/detailed-results/`, {
          headers: { Authorization: `Token ${token}` }
        });
        this.detailedResults = res.data;
      } catch {
        this.detailedResults = null;
      }
    },
    exportToCSV() {
      if (!this.detailedResults) return;
      const questions = this.detailedResults.questions;
      const rows = [
        ['Пользователь', ...questions, 'Баллы', 'Дата прохождения']
      ];
      this.detailedResults.results.forEach(user => {
        const answerCells = user.answers.map(ans => {
          let mark = ans.is_correct ? '✔' : '✘';
          if (ans.user_answer) mark += ` (${ans.user_answer})`;
          return mark;
        });
        rows.push([
          user.username,
          ...answerCells,
          user.score,
          this.formatDate(user.completed_at)
        ]);
      });
      const csvContent = rows.map(r => r.map(cell => '"' + String(cell).replace(/"/g, '""') + '"').join(',')).join('\n');
      const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
      const link = document.createElement('a');
      link.href = URL.createObjectURL(blob);
      link.setAttribute('download', 'test_results.csv');
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    }
  }
}
</script>

<style scoped>
.results-page {
  max-width: 900px;
  margin: 2rem auto;
}
.table td, .table th {
  text-align: center;
}
</style>
