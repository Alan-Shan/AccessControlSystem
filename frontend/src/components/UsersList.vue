<template>
  <div class="container">
    <div class="row">
      <div class="col-md-12">
        <h1>Список пользователей</h1>
        <div v-if="loading" class="d-flex justify-content-center w-100 mt-5 mb-5">
          <div class="spinner-grow" role="status">
          </div>
        </div>
        <div v-if="message.text" class="alert" :class="alertClass" role="alert">
          {{ message.text }}
        </div>
        <table v-if="!loading" class="table table-striped">
          <thead>
          <tr>
            <th scope="col">Имя пользователя</th>
            <th scope="col">Тип</th>
            <th scope="col">Действия</th>
          </tr>
          </thead>
          <tbody>
          <tr v-for="user in users" :key="user.id">
            <td>{{ user.username }}</td>
            <td>{{user.admin_type === 'admin' ? 'Администратор' :
                    'Господь Бог'
              }}
            </td>
            <td>
              <div class="btn-group" role="group">
                <button type="button" class="btn btn-primary" @click="editUser(user.id)">
                  <font-awesome-icon icon="user-edit"/>
                </button>
                <button type="button" class="btn btn-danger" @click="deleteUser(user.id)">
                  <font-awesome-icon icon="user-minus"/>
                </button>
              </div>
            </td>
          </tr>
          </tbody>
        </table>
        <button @click="editUser(null)" class="btn btn-primary">
          <font-awesome-icon icon="plus"/>
          Добавить пользователя
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import api from "@/services/api";

export default {
  name: "UsersList",
  data() {
    return {
      users: [],
      loading: true,
      message: {
        text: "",
        isError: false,
      },
    }
  },
  computed: {
    alertClass() {
      return {
        "alert-danger": this.message.isError,
        "alert-success": !this.message.isError,
      }
    },
  },
  async mounted() {
    try {
      const response = await api.getAdmins();
      this.users = response.data;
      console.debug(this.users);
    } catch (e) {
      this.message.text = "Ошибка при получении списка пользователей";
      this.message.isError = true;
    } finally {
      this.loading = false;
    }
  },
  methods: {
    editUser(id) {
      this.$router.push({name: "SingleUser", params: {id: id}});
    },
    async deleteUser(id) {
      try {
        await api.deleteAdmin(id);
        this.users = this.users.filter(user => user.id !== id);
        this.message = {
          text: "Пользователь успешно удален",
          isError: false,
        };
      } catch (e) {
        this.message.text = "Ошибка при удалении пользователя";
        this.message.isError = true;
      }
    }
  }
}
</script>

<style scoped>

</style>