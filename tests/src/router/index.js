import { createRouter, createWebHistory } from 'vue-router'
import SignUp from '@/views/SignUp.vue'
import LogIn from '@/views/LogIn.vue'
import TestCreator from '@/views/TestCreator.vue'
import TestExecutor from '@/views/TestExecutor'
import Profile from '@/views/Profile.vue'
import Results from '@/views/Results.vue'



const routes = [
  {
    path: '/signup',
    name: 'SignUp',
    component: SignUp
  },
  {
    path: '/login',
    name: 'LogIn',
    component: LogIn
  },
  {
    path: '/testcreator',
    name: 'TestCreator',
    component: TestCreator
  },
  {
    path: '/testexecutor',
    name: 'TestExecutor',
    component: TestExecutor
  },
  {
    path: '/profile',
    name: 'Profile',
    component: Profile
  },
  {
    path: '/results',
    name: 'Results',
    component: Results
  },
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

// Глобальный guard: разрешаем только /login и /signup без токена
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token')
  const publicPages = ['/login', '/signup']
  const authRequired = !publicPages.includes(to.path)

  if (authRequired && !token) {
    next({ path: '/login', query: { redirected: '1' } })
  } else {
    next()
  }
})

export default router
