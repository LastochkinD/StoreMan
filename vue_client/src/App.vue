<template>
  <div id="main">
    <!-- Меню -->
    <header class="menu">
      <nav>
        <ul>
          <li><router-link to="/">Главная</router-link></li>
          <li><router-link to="/clients">Клиенты</router-link></li>
          <li><router-link to="/products">Товары</router-link></li>
        </ul>
      </nav>
    </header>

    <!-- Рабочая область -->
    <router-view></router-view>

    <!-- Footer -->
    <footer>
      <p>&copy; 2023 Управление продажами. Все права защищены.</p>
    </footer>
  </div>
</template>

<script>
import { RouterLink, RouterView } from 'vue-router';

export default {
  components: {
    RouterLink,
    RouterView
  },
  name: 'Main',
  // В этом месте можно добавить логику, связанную с приложением
}
</script>

<style>
/* Стили для меню, рабочей области и footer могут быть добавлены здесь */
body {
  font-family: Arial, sans-serif;
  margin: 0;
  padding: 0;
}

#main {
  text-align: center;
}

.menu {
  background-color: #333;
  color: white;
  padding: 1rem;
}

.menu nav ul {
  list-style: none;
  padding: 0;
  display: flex;
  justify-content: center;
}

.menu nav ul li {
  margin: 0 20px;
}

.menu nav ul li:last-child {
  margin-right: 0;
}

footer {
  background-color: #333;
  color: white;
  padding: 1rem;
  position: fixed;
  bottom: 0;
  width: 100%;
}
</style>