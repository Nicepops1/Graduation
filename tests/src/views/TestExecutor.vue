<template>
  <div class="test-executor box">
    <h1 class="title is-3 has-text-centered">Прохождение теста</h1>
    <div v-if="!selectedTest">
      <div v-if="loading" class="has-text-centered">Загрузка тестов...</div>
      <div v-else>
        <div class="field" style="position:relative;">
          <label class="label">Поиск теста</label>
          <div class="control has-icons-left">
            <input class="input" type="text" v-model="searchQuery" placeholder="Введите название теста..." autocomplete="off" @focus="showSuggestions = true" @blur="hideSuggestions" @input="showSuggestions = true">
            <span class="icon is-left"><i class="fas fa-search"></i></span>
          </div>
          <div v-if="showSuggestions && filteredTests.length" class="box" style="position: absolute; z-index: 10; width: 100%; max-height: 200px; overflow-y: auto;">
            <div v-for="test in filteredTests" :key="test.id" class="dropdown-item" :class="{'has-background-info-light': test.id === selectedTestId}" @mousedown.prevent="selectTest(test)">
              {{ test.title }}
            </div>
          </div>
        </div>
        <button class="button is-primary is-fullwidth mt-4" :disabled="!selectedTestId" @click="loadTest">Начать тест</button>
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
      resultMessage: '',
      searchQuery: '',
      showSuggestions: false
    };
  },
  created() {
    this.fetchTests();
  },
  methods: {
    async fetchTests() {
      this.loading = true;
      try {
        const token = localStorage.getItem('token');
        const res = await axios.get('http://127.0.0.1:8000/api/v1/tests/', {
          headers: { Authorization: `Token ${token}` }
        });
        this.tests = res.data;
      } catch (e) {
        this.tests = [];
      }
      this.loading = false;
    },
    selectTest(test) {
      this.selectedTestId = test.id;
      this.searchQuery = test.title;
      this.showSuggestions = false;
    },
    hideSuggestions() {
      setTimeout(() => { this.showSuggestions = false; }, 150);
    },
    async loadTest() {
      this.selectedTest = null;
      this.userAnswers = [];
      this.resultMessage = '';
      try {
        const token = localStorage.getItem('token');
        const res = await axios.get(`http://127.0.0.1:8000/api/v1/tests/${this.selectedTestId}/`, {
          headers: { Authorization: `Token ${token}` }
        });
        this.selectedTest = {
          ...res.data,
          questions: res.data.questions.map(q => ({
            ...q,
            type: q.question_type,
            options: q.options || []
          }))
        };
        this.userAnswers = this.selectedTest.questions.map(q => {
          if (q.type === 'multiple') return [];
          return '';
        });
      } catch (e) {
        this.selectedTest = null;
      }
    },
    async submitAnswers() {
      // Собираем ответы в нужном формате для бэкенда
      const answers = this.selectedTest.questions.map((q, idx) => {
        if (q.type === 'single') {
          // userAnswers[idx] — индекс выбранного варианта
          const selectedIdx = this.userAnswers[idx];
          const answerId = q.options[selectedIdx]?.id;
          return {
            question_id: q.id,
            answer_ids: answerId !== undefined ? [answerId] : []
          };
        } else if (q.type === 'multiple') {
          // userAnswers[idx] — массив индексов выбранных вариантов
          const selectedIdxs = this.userAnswers[idx] || [];
          const answerIds = selectedIdxs.map(i => q.options[i]?.id).filter(Boolean);
          return {
            question_id: q.id,
            answer_ids: answerIds
          };
        } else if (q.type === 'text') {
          return {
            question_id: q.id,
            text: this.userAnswers[idx]
          };
        }
        return null;
      }).filter(Boolean);
      try {
        const token = localStorage.getItem('token');
        await axios.post('http://127.0.0.1:8000/api/v1/tests/submit/', {
          test_id: this.selectedTestId,
          answers
        }, {
          headers: { Authorization: `Token ${token}` }
        });
        this.resultMessage = 'Ответы успешно отправлены!';
        setTimeout(() => {
          this.selectedTest = null;
          this.selectedTestId = '';
          this.userAnswers = [];
          this.resultMessage = '';
          this.searchQuery = '';
        }, 1200);
      } catch (e) {
        this.resultMessage = 'Ошибка при отправке ответов.';
      }
    }
  },
  computed: {
    filteredTests() {
      const q = this.searchQuery.trim().toLowerCase();
      if (!q) return this.tests;
      return this.tests.filter(t => t.title.toLowerCase().includes(q));
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
.field label.radio,
.field label.checkbox {
  word-break: break-word;
  white-space: normal;
  display: flex;
  align-items: flex-start;
}
.field label.radio input,
.field label.checkbox input {
  margin-top: 0.2em;
  margin-right: 0.5em;
}
</style>
