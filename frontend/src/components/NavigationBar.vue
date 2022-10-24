<template>

  <nav class="navbar navbar-expand-lg navbar-dark bg-primary bd-navbar sticky-top">
    <a class="navbar-brand">
      <img src="/favicon.ico" width="30" height="30" class="d-inline-block align-top" alt="">
      OGate
    </a>
    <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNavDropdown"
            aria-controls="navbarNavDropdown" aria-expanded="false" aria-label="Toggle navigation">
      <span class="navbar-toggler-icon"></span>
    </button>
    <div class="collapse navbar-collapse" id="navbarNavDropdown">
      <ul class="navbar-nav">
        <li class="nav-item active">
          <router-link to="/">
            <span class="nav-link">Главная </span>
          </router-link>
        </li>
      </ul>
      <ul class="navbar-nav me-auto" id="privileged_block" v-if="hasPrivilegedAccess">
        <li class="nav-item">
          <router-link to="/">
            <span class="nav-link">Админ-панель</span>
          </router-link>
        </li>
        <li class="nav-item">
          <router-link to="/">
            <span class="nav-link">Заявки </span>
          </router-link>
        </li>
        <li v-if="isSuperAdmin" class="nav-item">
          <router-link to="/">
            <span class="nav-link">Пользователи</span>
          </router-link>
        </li>
      </ul>
      <ul class="navbar-nav">
        <li v-if="user.identity" class="nav-item dropdown">
          <a class="nav-link dropdown-toggle" @click="openOrCloseDropdown" href="#" id="navbarDropdownMenuLink"
             data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
            {{ user.identity }} ({{ user.role }})
          </a>
          <div class="dropdown-menu" :class="{'show': dropdownIsOpen}" aria-labelledby="navbarDropdownMenuLink">
            <a class="dropdown-item">Настройки</a>
            <span class="dropdown-item" @click="logout">Выход из системы</span>
          </div>
        </li>
      </ul>
    </div>
  </nav>
</template>

<script>

import router from "@/router";

export default {
  name: "NavigationBar",
  data() {
    return {
      dropdownIsOpen: false
    }
  },
  computed: {
    user() {
      return {
        identity: this.$store.getters["auth/getCurrentUsername"],
        role: this.$store.getters['auth/getCurrentRole'],
      };
    },
    hasPrivilegedAccess() {
      return this.$store.getters['auth/hasPrivilegedAccess'];
    },
    isSuperAdmin() {
      return this.$store.getters['auth/isSuperAdmin'];
    },
  },
  methods: {
    openOrCloseDropdown() {
      this.dropdownIsOpen = !this.dropdownIsOpen;
    },
    logout() {
      this.$store.dispatch("auth/logout").then(() => {
        router.push({name: "Login"});
      });
    }
  }
}
</script>

<style scoped>
.dropdown-item {
  cursor: pointer;
}
.navbar {
  margin: 0 0 3rem 0;
  padding: 0.5rem 1rem;
  box-shadow: 0 0.5rem 1rem rgb(0 0 0 / 15%), inset 0 -1px 0 rgb(0 0 0 / 15%);;
}
</style>