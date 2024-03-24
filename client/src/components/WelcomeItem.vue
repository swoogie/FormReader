<template>
  <div class="flex first:mt-8 mt-5 bg-zinc-100 rounded-md p-3 dark:bg-zinc-800">
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
