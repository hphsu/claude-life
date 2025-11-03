import { apiClient } from './client';
import type {
  Order,
  CreateOrderInput,
  ExpertSystemInfo,
  PaginatedResponse,
} from '@/types/api';

const ORDERS_ENDPOINT = '/api/orders/';
const EXPERT_SYSTEMS_ENDPOINT = '/api/expert-systems/';

export const ordersApi = {
  // Get all orders (paginated)
  getAll: async (page = 1, pageSize = 20): Promise<PaginatedResponse<Order>> => {
    const response = await apiClient.get<PaginatedResponse<Order>>(
      ORDERS_ENDPOINT,
      {
        params: { page, page_size: pageSize },
      }
    );
    return response.data;
  },

  // Get single order by ID
  getById: async (id: string): Promise<Order> => {
    const response = await apiClient.get<Order>(`${ORDERS_ENDPOINT}${id}/`);
    return response.data;
  },

  // Create new order
  create: async (data: CreateOrderInput): Promise<Order> => {
    const response = await apiClient.post<Order>(ORDERS_ENDPOINT, data);
    return response.data;
  },

  // Get available expert systems with pricing
  getExpertSystems: async (): Promise<ExpertSystemInfo[]> => {
    const response = await apiClient.get<ExpertSystemInfo[]>(
      EXPERT_SYSTEMS_ENDPOINT
    );
    return response.data;
  },

  // Calculate order price with discounts
  calculatePrice: async (
    expertSystems: string[]
  ): Promise<{ total: number; discount: number; final: number }> => {
    const response = await apiClient.post<{
      total: number;
      discount: number;
      final: number;
    }>(`${ORDERS_ENDPOINT}calculate-price/`, {
      expert_systems: expertSystems,
    });
    return response.data;
  },
};
