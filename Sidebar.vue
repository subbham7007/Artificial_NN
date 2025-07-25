<script setup lang="ts">
/**
 * The sidebar component implements the sidebar that is shown on any workspace
 * page. It contains links to the different sections of the workspace.
*/
const multisite = ref(true)

const config = useRuntimeConfig()
multisite.value = getBoolean(config.public.multisite)

const sidebarStore = useSidebarStore()
const projectStore = useProjectStore()

interface IconSize { section: number, page: number }
const iconSize = ref<IconSize>({ section: 22, page: 16 })

// Reactive states for tracking collapse sections
const collapseStates = ref({
  data: false,
  multisite: false,
  schema: false,
  serverless: false,
  project: false
})

/**
 * Computed property that returns the URL for the given workspace path. Returns
 * an empty string until the projects are loaded and available.
 * @param { string } path The workspace path.
 */
const url = computed(() => (path: string) => {
  if (!projectStore.active) return ''

  return `/workspace/${projectStore.active}/${path}`
})

// Event handlers for collapse state changes
const handleCollapseToggle = (section: keyof typeof collapseStates.value) => {
  collapseStates.value[section] = !collapseStates.value[section]
}

// Listen to Bootstrap collapse events to sync state
onMounted(() => {
  const sections = ['data', 'multisite', 'schema', 'serverless', 'project']
  
  sections.forEach(section => {
    const element = document.getElementById(`collapse-${section}`)
    if (element) {
      element.addEventListener('shown.bs.collapse', () => {
        collapseStates.value[section as keyof typeof collapseStates.value] = true
      })
      element.addEventListener('hidden.bs.collapse', () => {
        collapseStates.value[section as keyof typeof collapseStates.value] = false
      })
    }
  })
})
</script>

<template>
  <div class="wrapper">
    <nav id="sidebar" :class="{ active: sidebarStore.open }">
      <div class="close-button">
        <div id="cancel-icon" @click="sidebarStore.open = false">
          <Icon name="bi:x" size="35" />
        </div>
      </div>
      <!-- Sidebar Menus -->
      <ul class="list-unstyled components">
        <!-- Data Section -->
        <li>
          <a 
            v-b-toggle.collapse-data 
            :aria-expanded="collapseStates.data" 
            class="dropdown-toggle"
            @click="handleCollapseToggle('data')"
          >
            <Icon class="icon mr-2" name="bi:server" :size="iconSize.section" />
            {{ $t('sidebar.data.main') }}
          </a>
          <BCollapse id="collapse-data">
            <ul class="list-unstyled">
              <li>
                <NuxtLink :to="{ path: url('data/search') }">
                  <Icon class="icon mr-2" name="bi:search" :size="iconSize.page" />
                  {{ $t('sidebar.data.search') }}
                </NuxtLink>
              </li>
              <li>
                <AccessLimit resource="artifacts" permission="write" hide-tooltip>
                  <NuxtLink :to="{ path: url('data/upload') }">
                    <Icon class="icon mr-2" name="bi:upload" :size="iconSize.page" />
                    {{ $t('sidebar.data.upload') }}
                  </NuxtLink>
                </AccessLimit>
              </li>
            </ul>
          </BCollapse>
        </li>
        <!-- /Data Section -->

        <!-- Multisite Section -->
        <li v-if="multisite">
          <a 
            v-b-toggle.collapse-multisite 
            :aria-expanded="collapseStates.multisite" 
            class="dropdown-toggle"
            @click="handleCollapseToggle('multisite')"
          >
            <Icon class="mr-2 icon" name="bi:diagram-3-fill" :size="iconSize.section" />
            {{ $t('sidebar.multisite.main') }}
          </a>
          <BCollapse id="collapse-multisite">
            <ul class="list-unstyled">
              <li>
                <AccessLimit resource="replication-policies" permission="read" hide-tooltip>
                  <NuxtLink :to="{ path: url('multisite/replication') }">
                    <Icon class="mr-2" name="bi:card-list" :size="iconSize.page" />
                    {{ $t('sidebar.multisite.replicationPolicies') }}
                  </NuxtLink>
                </AccessLimit>
              </li>
            </ul>
          </BCollapse>
        </li>
        <!-- /Multisite Section -->

        <!-- Schema Section -->
        <li>
          <a 
            v-b-toggle.collapse-schema 
            :aria-expanded="collapseStates.schema" 
            class="dropdown-toggle"
            @click="handleCollapseToggle('schema')"
          >
            <Icon class="mr-2 icon" name="bi:file-earmark-text-fill" :size="iconSize.section" />
            {{ $t('sidebar.schemas.main') }}
          </a>
          <BCollapse id="collapse-schema">
            <ul class="list-unstyled">
              <li>
                <AccessLimit resource="schemas" permission="read" hide-tooltip>
                  <NuxtLink :to="{ path: url('schemas') }">
                    <Icon class="icon mr-2" name="bi:file-earmark-text" :size="iconSize.page" />
                    {{ $t('sidebar.schemas.overview') }}
                  </NuxtLink>
                </AccessLimit>
              </li>
            </ul>
          </BCollapse>
        </li>
        <!-- /Schema Section -->

        <!-- Serverless Section -->
        <li>
          <a 
            v-b-toggle.collapse-serverless 
            :aria-expanded="collapseStates.serverless" 
            class="dropdown-toggle"
            @click="handleCollapseToggle('serverless')"
          >
            <Icon class="icon mr-2" name="bi:hdd-stack-fill" :size="iconSize.section" />
            {{ $t('sidebar.serverless.main') }}
          </a>
          <BCollapse id="collapse-serverless">
            <ul class="list-unstyled">
              <li>
                <AccessLimit resource="serverless" permission="read" hide-tooltip>
                  <NuxtLink :to="{ path: url('serverless/functions') }">
                    <Icon class="icon mr-2" name="bi:code-slash" :size="iconSize.page" />
                    {{ $t('sidebar.serverless.functions') }}
                  </NuxtLink>
                </AccessLimit>
              </li>
              <li>
                <AccessLimit resource="triggers" permission="read" hide-tooltip>
                  <NuxtLink :to="{ path: url('serverless/triggers') }">
                    <Icon class="icon mr-2" name="bi:gear" :size="iconSize.page" />
                    {{ $t('sidebar.serverless.triggers') }}
                  </NuxtLink>
                </AccessLimit>
              </li>
            </ul>
          </BCollapse>
        </li>
        <!-- /Serverless Section -->

        <!-- Project Section -->
        <li>
          <a 
            v-b-toggle.collapse-project 
            :aria-expanded="collapseStates.project" 
            class="dropdown-toggle"
            @click="handleCollapseToggle('project')"
          >
            <Icon class="icon mr-2" name="bi:file-earmark-break-fill" size="20" />
            {{ $t('sidebar.project.main') }}
          </a>
          <BCollapse id="collapse-project">
            <ul class="list-unstyled">
              <li>
                <AccessLimit resource="logs" permission="read" hide-tooltip>
                  <NuxtLink :to="{ path: url('project/activity') }">
                    <Icon class="icon mr-2" name="bi:justify-left" size="16" />
                    {{ $t('sidebar.project.activity') }}
                  </NuxtLink>
                </AccessLimit>
              </li>
            </ul>
          </BCollapse>
        </li>
        <!-- /Project Section -->
      </ul>
      <!-- /Sidebar Menus -->
    </nav>

    <div :class="{ active: sidebarStore.open }" class="sidebar-backdrop" @click="sidebarStore.open = false" />
  </div>
</template>

<style lang="scss" scoped>
a {
  color: inherit;
  text-decoration: none;
  transition: all 0.3s;
}

.wrapper {
  height: 100%;
}

.icon {
  vertical-align: sub;
}

#sidebar {
  min-width: rem.convert(220px);
  max-width: rem.convert(220px);
  height: 100%;
  position: relative;
  background: #f9f9f9;
  color: #000;
  transition: all 0.3s;

  ul.components {
    padding: 1.25rem 0;
  }

  ul {
    p {
      color: #000;
      padding: 10px;
    }

    li {
      a {
        padding: 0.625rem;
        font-size: 1.1rem;
        display: block;

        &:hover {
          text-shadow: 0 0 0.5px black;
        }
      }
    }

    li.active {
      > a {
        color: #000;
        background: #dfe1e5;
      }
    }
  }
}

.dropdown-toggle {
  position: relative;
  cursor: pointer;

  &::after {
    content: '▶';
    display: block;
    position: absolute;
    top: 50%;
    right: rem.convert(20px);
    transition: transform 0.35s ease;
    transform: translateY(-50%) rotate(-90deg);
    font-size: 0.8rem;
  }

  &[aria-expanded='true']::after {
    transform: translateY(-50%) rotate(0deg);
  }
}

ul {
  ul {
    a {
      font-size: 1em !important;
      padding-left: 2rem !important;
      background: #f9f9f9;
    }
  }
}

.router-link-active {
  color: #000;
  background: #c6dcd6;
}

#cancel-icon {
  display: none;
}

@media (max-width: 768px) {
  #sidebar {
    position: fixed;
    top: 0;
    left: rem.convert(-220px);
    z-index: 999;

    &.active {
      left: 0;
    }
  }

  .sidebar-backdrop {
    display: none;
    position: fixed;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.7);
    z-index: 998;
    opacity: 0;
    transition: all 0.5s ease-in-out;

    &.active {
      display: block;
      opacity: 1;
      top: 0;
    }
  }

  #cancel-icon {
    display: block;
    cursor: pointer;
    margin-left: auto;
    margin-right: 0;

    &:hover {
      color: rgb(70, 70, 70);
    }
  }

  ul.list-unstyled {
    padding-top: rem.convert(10px) !important;
  }
  .close-button {
    display: flex;
    padding-right: rem.convert(10px);
  }
}
</style>