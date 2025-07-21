<template>
  <div id="wrapper">
    <nav class="navbar is-dark">
    <div class="navbar-brand">
      <router-link to="/" class="navbar-item"><strong>TESTS</strong></router-link>

      <a href="" class="navbar-burger" aria-label="menu" aria-expanded="false" data-target="navbar-menu">
        <span aria-hidden="true"></span>
        <span aria-hidden="true"></span>
        <span aria-hidden="true"></span>
      </a>
    </div>
    <div class="navbar-menu" id="navbar-menu">
      <div class="navbar-end">
        <router-link to="/profile" class="navbar-item">Профиль</router-link>
        <router-link to="/testcreator" class="navbar-item">Создать тест</router-link>
        <router-link to="/testexecutor" class="navbar-item">Тестирование</router-link>
        <router-link to="/results" class="navbar-item">Результаты</router-link>

      </div>
    </div>
  </nav>
  </div>
  <section class="section">
    <router-view/>
  </section>
  
</template>

<style lang="scss">
@import '../../node_modules/bulma/';
</style>
