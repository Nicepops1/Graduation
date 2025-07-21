<template>
  <div class="test-creator box">
    <h1 class="title is-3 has-text-centered">Конструктор тестов</h1>
    <form @submit.prevent="submitTest">
      <div class="field">
        <label class="label">Название теста</label>
        <div class="control">
          <input class="input" v-model="testTitle" required placeholder="Введите название теста" />
        </div>
      </div>
      <div v-for="(question, qIdx) in questions" :key="qIdx" class="box question-block">
        <div class="level">
          <div class="level-left">
            <h3 class="subtitle is-5">Вопрос {{ qIdx + 1 }}</h3>
          </div>
          <div class="level-right">
            <button type="button" class="delete is-medium" @click="removeQuestion(qIdx)" v-if="questions.length > 1"></button>
          </div>
        </div>
        <div class="field">
          <label class="label">Текст вопроса</label>
          <div class="control">
            <input class="input" v-model="question.text" placeholder="Введите текст вопроса" required />
          </div>
        </div>
        <div class="field">
          <label class="label">Тип вопроса</label>
          <div class="control">
            <div class="select">
              <select v-model="question.type">
                <option value="single">Один вариант</option>
                <option value="multiple">Несколько вариантов</option>
                <option value="text">Свободный ответ</option>
              </select>
            </div>
          </div>
        </div>
        <div v-if="question.type === 'single' || question.type === 'multiple'">
          <label class="label">Варианты ответов</label>
          <div v-for="(option, oIdx) in question.options" :key="oIdx" class="field has-addons option-block">
            <div class="control">
              <template v-if="question.type === 'single'">
                <input type="radio"
                  :name="'single-correct-' + qIdx"
                  class="mr-2"
                  :checked="option.correct"
                  @change="setSingleCorrect(qIdx, oIdx)"
                />
              </template>
              <template v-else>
                <input type="checkbox"
                  class="mr-2"
                  v-model="option.correct"
                />
              </template>
            </div>
            <div class="control is-expanded">
              <input class="input" v-model="option.text" placeholder="Вариант ответа" required />
            </div>
            <div class="control">
              <button type="button" class="button is-danger" @click="removeOption(qIdx, oIdx)" v-if="question.options.length > 1">
                <span class="icon is-small"><i class="fas fa-times"></i></span>
              </button>
            </div>
          </div>
          <button type="button" class="button is-link is-light mb-3" @click="addOption(qIdx)">
            <span class="icon is-small"><i class="fas fa-plus"></i></span>
            <span>Добавить вариант</span>
          </button>
        </div>
        <div v-else-if="question.type === 'text'">
          <div class="notification is-info is-light mb-2">
            Ответ на этот вопрос пользователь должен будет написать самостоятельно.
          </div>
          <div class="field">
            <label class="label">Правильный ответ</label>
            <div class="control">
              <input class="input" v-model="question.correctAnswer" placeholder="Введите правильный ответ" required />
            </div>
          </div>
        </div>
      </div>
      <button type="button" class="button is-primary is-fullwidth mb-4" @click="addQuestion">
        <span class="icon is-small"><i class="fas fa-plus"></i></span>
        <span>Добавить вопрос</span>
      </button>
      <button type="submit" class="button is-success is-fullwidth">Создать тест</button>
    </form>
    <div v-if="successMessage" class="notification is-success mt-4">{{ successMessage }}</div>
    <div v-if="errorMessage" class="notification is-danger mt-4">{{ errorMessage }}</div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'TestCreator',
  data() {
    return {
      testTitle: '',
      questions: [
        {
          text: '',
          type: 'single',
          options: [
            { text: '', correct: false },
            { text: '', correct: false }
          ],
          correctAnswer: '' // для text-вопроса
        }
      ],
      successMessage: '',
      errorMessage: ''
    };
  },
  methods: {
    addQuestion() {
      this.questions.push({
        text: '',
        type: 'single',
        options: [
          { text: '', correct: false },
          { text: '', correct: false }
        ],
        correctAnswer: ''
      });
    },
    removeQuestion(qIdx) {
      this.questions.splice(qIdx, 1);
    },
    addOption(qIdx) {
      this.questions[qIdx].options.push({ text: '', correct: false });
    },
    removeOption(qIdx, oIdx) {
      this.questions[qIdx].options.splice(oIdx, 1);
    },
    setSingleCorrect(qIdx, oIdx) {
      this.questions[qIdx].options.forEach((opt, idx) => {
        opt.correct = idx === oIdx;
      });
    },
    async submitTest() {
      this.successMessage = '';
      this.errorMessage = '';
      // Формируем структуру для отправки
      const questionsToSend = this.questions.map(q => {
        if (q.type === 'text') {
          return {
            text: q.text,
            type: q.type,
            options: [],
            correctAnswer: q.correctAnswer
          };
        } else {
          return {
            text: q.text,
            type: q.type,
            options: q.options.map(opt => ({ text: opt.text, correct: !!opt.correct })),
            correctAnswer: ''
          };
        }
      });
      const payload = {
        title: this.testTitle,
        questions: questionsToSend
      };
      try {
        await axios.post('/api/tests/create', payload);
        this.successMessage = 'Тест успешно создан!';
        this.testTitle = '';
        this.questions = [{
          text: '',
          type: 'single',
          options: [
            { text: '', correct: false },
            { text: '', correct: false }
          ],
          correctAnswer: ''
        }];
      } catch (error) {
        this.errorMessage = 'Ошибка при создании теста.';
      }
    }
  }
};
</script>

<style scoped>
.test-creator {
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
.option-block {
  margin-bottom: 0.5rem;
}
</style>
