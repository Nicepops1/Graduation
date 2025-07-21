<template>
  <div class="test-executor box">
    <h1 class="title is-3 has-text-centered">Прохождение теста</h1>
    <div v-if="!selectedTest">
      <div v-if="loading" class="has-text-centered">Загрузка тестов...</div>
      <div v-else>
        <div class="field">
          <label class="label">Выберите тест для прохождения</label>
          <div class="control">
            <div class="select is-fullwidth">
              <select v-model="selectedTestId">
                <option disabled value="">-- Выберите тест --</option>
                <option v-for="test in tests" :key="test.id" :value="test.id">{{ test.title }}</option>
              </select>
            </div>
          </div>
        </div>
        <button class="button is-primary is-fullwidth" :disabled="!selectedTestId" @click="loadTest">Начать тест</button>
      </div>
    </div>
    <div v-else>
      <h2 class="subtitle is-4 mb-4">{{ selectedTest.title }}</h2>
      <form @submit.prevent="submitAnswers">
        <div v-for="(question, qIdx) in selectedTest.questions" :key="qIdx" class="box question-block">
          <div class="mb-2"><b>Вопрос {{ qIdx + 1 }}:</b> {{ question.text }}</div>
          <div v-if="question.type === 'single'">
            <div v-for="(option, oIdx) in question.options" :key="oIdx" class="field">
              <label class="radio">
                <input type="radio" :name="'q' + qIdx" :value="oIdx" v-model="userAnswers[qIdx]" />
                {{ option.text }}
              </label>
            </div>
          </div>
          <div v-else-if="question.type === 'multiple'">
            <div v-for="(option, oIdx) in question.options" :key="oIdx" class="field">
              <label class="checkbox">
                <input type="checkbox" :value="oIdx" v-model="userAnswers[qIdx]" />
                {{ option.text }}
              </label>
            </div>
          </div>
          <div v-else-if="question.type === 'text'">
            <input class="input" v-model="userAnswers[qIdx]" placeholder="Введите ваш ответ" />
          </div>
        </div>
        <button type="submit" class="button is-success is-fullwidth mt-3">Отправить ответы</button>
      </form>
      <div v-if="resultMessage" class="notification is-info mt-4">{{ resultMessage }}</div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'TestExecutor',
  data() {
    return {
      tests: [],
      loading: false,
      selectedTestId: '',
      selectedTest: null,
      userAnswers: [],
      resultMessage: ''
    };
  },
  created() {
    this.fetchTests();
  },
  methods: {
    async fetchTests() {
      this.loading = true;
      try {
        const res = await axios.get('/api/tests/');
        this.tests = res.data;
      } catch (e) {
        this.tests = [];
      }
      this.loading = false;
    },
    async loadTest() {
      this.selectedTest = this.tests.find(t => t.id === this.selectedTestId);
      // Инициализация ответов
      this.userAnswers = this.selectedTest.questions.map(q => {
        if (q.type === 'multiple') return [];
        return '';
      });
      this.resultMessage = '';
    },
    async submitAnswers() {
      // Формируем структуру для отправки
      const answers = this.selectedTest.questions.map((q, idx) => {
        if (q.type === 'multiple') {
          return { question: q.text, answer: this.userAnswers[idx] };
        } else if (q.type === 'single') {
          return { question: q.text, answer: this.userAnswers[idx] };
        } else {
          return { question: q.text, answer: this.userAnswers[idx] };
        }
      });
      try {
        await axios.post('/api/tests/submit', {
          testId: this.selectedTest.id,
          answers
        });
        this.resultMessage = 'Ответы успешно отправлены!';
      } catch (e) {
        this.resultMessage = 'Ошибка при отправке ответов.';
      }
    }
  }
};
</script>

<style scoped>
.test-executor {
  max-width: 700px;
  margin: 2rem auto;
  background: #fff;
}
.question-block {
  margin-bottom: 1.5rem;
  border: 1px solid #eaeaea;
  border-radius: 8px;
  background: #f8f8f8;
}
</style>
