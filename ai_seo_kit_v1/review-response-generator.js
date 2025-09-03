#!/usr/bin/env node
/*
 * review-response-generator.js
 *
 * A simple Node.js script to generate multiple response variations for a given
 * customer review. The script reads a review from standard input or from a
 * provided argument and returns three suggested responses tailored to the
 * sentiment of the review. These responses are designed to be empathetic,
 * professional and helpful, encouraging the reviewer to stay engaged.
 *
 * Usage:
 *   node review-response-generator.js "This coffee shop had terrible service"
 *
 * Or run without arguments and follow the prompt to enter a review.
 */

const readline = require('readline');

// Basic lists of positive and negative words to infer sentiment
const positiveWords = [
  'good', 'great', 'excellent', 'amazing', 'fantastic', 'love', 'loved', 'wonderful'
];
const negativeWords = [
  'bad', 'terrible', 'poor', 'awful', 'horrible', 'hate', 'worst', 'disappointed'
];

/**
 * Determine the sentiment of a review by counting positive and negative words.
 * Returns "positive", "negative" or "neutral".
 * @param {string} review
 */
function detectSentiment(review) {
  const text = review.toLowerCase();
  let posCount = 0;
  let negCount = 0;
  positiveWords.forEach(word => {
    if (text.includes(word)) posCount++;
  });
  negativeWords.forEach(word => {
    if (text.includes(word)) negCount++;
  });
  if (posCount > negCount) return 'positive';
  if (negCount > posCount) return 'negative';
  return 'neutral';
}

/**
 * Generate response variations based on the review and its sentiment.
 * @param {string} review
 */
function generateResponses(review) {
  const sentiment = detectSentiment(review);
  const base = 'Thank you for your feedback';
  const namePlaceholder = 'Dear customer';

  // Response templates for different sentiments
  const templates = {
    positive: [
      `${base}! We’re thrilled to hear you enjoyed your experience. If there’s anything else we can do for you, please let us know.`,
      `${base}. Your support means a lot to us. We hope to see you again soon!`,
      `${base}! It makes our day to read a review like this. Thanks for choosing us.`
    ],
    negative: [
      `${base}. We’re sorry to hear about your experience and appreciate you bringing this to our attention. Please reach out so we can make it right.`,
      `${base}, and we’re very sorry that we missed the mark. We’d love the opportunity to learn more and improve.`,
      `${base}. We understand your frustration and would like to discuss how we can address your concerns.`
    ],
    neutral: [
      `${base}. We appreciate your honest feedback and hope to make your next visit even better.`,
      `${base}! Your insights help us grow and improve our services. Thank you for taking the time to share.`,
      `${base}. We’re always looking for ways to improve and your feedback guides us.`
    ]
  };

  const responses = templates[sentiment] || templates.neutral;
  return responses;
}

function main() {
  const args = process.argv.slice(2);
  if (args.length) {
    const review = args.join(' ');
    const responses = generateResponses(review);
    responses.forEach((r, i) => {
      console.log(`Response ${i + 1}: ${r}`);
    });
    return;
  }
  // Interactive prompt if no argument is provided
  const rl = readline.createInterface({ input: process.stdin, output: process.stdout });
  rl.question('Enter a customer review: ', (review) => {
    const responses = generateResponses(review);
    responses.forEach((r, i) => {
      console.log(`Response ${i + 1}: ${r}`);
    });
    rl.close();
  });
}

main();