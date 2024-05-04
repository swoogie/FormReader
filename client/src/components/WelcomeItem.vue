<template>
  <div class="flex mt-5 bg-zinc-200/50 rounded-md p-3 dark:bg-zinc-800/50">
    <i class="flex place-content-center place-items-center size-8">
      <slot name="icon"></slot>
    </i>
    <div class="flex-1 ml-4">
      <h3 class="text-xl font-medium mb-2">
        <slot name="heading"></slot>
      </h3>
      <slot></slot>
    </div>
  </div>
</template>
