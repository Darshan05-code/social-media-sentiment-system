/**
 * REST API client interacting with the Django backend endpoints.
 */

export const API_BASE = import.meta.env.VITE_API_BASE_URL || import.meta.env.VITE_API_URL || '/api';
export const DOCS_URL = `${API_BASE.replace(/\/api\/?$/, '')}/api/docs/`;

async function handleResponse(response) {
  if (!response.ok) {
    let errorData;
    try {
      errorData = await response.json();
    } catch {
      errorData = { error: `Server returned HTTP ${response.status}: ${response.statusText}` };
    }
    const error = new Error(errorData.error || errorData.message || 'Request failed');
    error.status = response.status;
    error.details = errorData.details || errorData;
    throw error;
  }
  return response.json();
}

export const api = {
  /** Health check */
  async checkHealth() {
    const res = await fetch(`${API_BASE}/health/`);
    return handleResponse(res);
  },

  /** Overview statistics */
  async getOverview() {
    const res = await fetch(`${API_BASE}/analytics/overview/`);
    return handleResponse(res);
  },

  /** Platform comparative metrics */
  async getComparison() {
    const res = await fetch(`${API_BASE}/analytics/comparison/`);
    return handleResponse(res);
  },

  /** Recent analyses list */
  async getRecentAnalyses(limit = 25) {
    const res = await fetch(`${API_BASE}/sentiment/?limit=${limit}`);
    return handleResponse(res);
  },

  /** Unified sentiment prediction */
  async predictSentiment({ platform, text, save_to_db = true, run_advanced_nlp = true }) {
    const res = await fetch(`${API_BASE}/sentiment/predict/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ platform, text, save_to_db, run_advanced_nlp }),
    });
    return handleResponse(res);
  },

  /** Social media credential status */
  async getSocialStatus() {
    const res = await fetch(`${API_BASE}/social/status/`);
    return handleResponse(res);
  },

  /** List ingested social posts */
  async getSocialPosts(platform = '', sentiment = '') {
    let url = `${API_BASE}/social/posts/?limit=50`;
    if (platform) url += `&platform=${encodeURIComponent(platform)}`;
    if (sentiment) url += `&sentiment=${encodeURIComponent(sentiment)}`;
    const res = await fetch(url);
    return handleResponse(res);
  },

  /** Trigger social fetch */
  async fetchSocialPosts({ platform, query = '', count = 10 }) {
    const res = await fetch(`${API_BASE}/social/fetch/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ platform, query, count }),
    });
    return handleResponse(res);
  }
};
