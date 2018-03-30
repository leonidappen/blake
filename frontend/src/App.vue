<template>
  <v-app>
    <template v-if="currentUser">
      <v-navigation-drawer app persistent clipped enable-resize-watcher :mini-variant="mini">
        <v-list>
          <v-list-tile router v-for="item in navigationDrawerItems" :to='item.action' :key="item.title">
            <v-list-tile-action>
              <v-icon v-html="item.icon"></v-icon>
            </v-list-tile-action>
            <v-list-tile-content>
              <v-list-tile-title v-text="item.title"></v-list-tile-title>
            </v-list-tile-content>
          </v-list-tile>
        </v-list>
      </v-navigation-drawer>

      <v-toolbar app :clipped-left="true">
        <v-toolbar-side-icon @click.stop="mini = !mini"></v-toolbar-side-icon>
        <v-toolbar-title v-text="title"></v-toolbar-title>
        <v-spacer></v-spacer>
        <v-menu offset-y>
          <v-btn flat  slot="activator">{{ currentUser.username }}</v-btn>
            <v-list>
              <v-list-tile router v-for="item in userMenuItems" :to='item.action' :key="item.title">
              <v-list-tile-title>{{ item.title }}</v-list-tile-title>
            </v-list-tile>
          </v-list>
        </v-menu>
      </v-toolbar>
    </template>
    
    <v-content>
      <router-view></router-view>
    </v-content>
  </v-app>
</template>

<script lang="ts">
import Vue from 'vue';

export default Vue.extend({
  name: 'App',
  data() {
    return {
      title: 'Blake',
      mini: true,
      currentUser: {
        username: 'handresen',
      },
      navigationDrawerItems: [
        { title: 'Dashboard', icon: 'dashboard', action: '/dashboard' },
        { title: 'Stores', icon: 'storage', action: '/stores' },
        { title: 'Scripts', icon: 'code', action: '/scripts' },
      ],
      userMenuItems: [
        { title: 'Logout', action: 'logout' },
      ],
    };
  },
});
</script>

