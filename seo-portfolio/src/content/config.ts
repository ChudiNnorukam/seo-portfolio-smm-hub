import { defineCollection, z } from 'astro:content'

const blog = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    description: z.string(),
    pubDate: z.coerce.date(),
    updatedDate: z.coerce.date().optional(),
    heroImage: z.string().optional(),
    tags: z.array(z.string()).default([]),
    canonical: z.string().optional(),
    author: z.string().default('Chudi Nnorukam'),
    category: z.string().optional(),
    section: z.string().optional(),
    featured: z.boolean().default(false),
    jsonLd: z.string().optional(), // For custom JSON-LD
  }),
})

export const collections = { blog }
