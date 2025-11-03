import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { ordersApi } from '@/services/api';
import { getErrorMessage } from '@/services/api/client';
import type {
  Order,
  CreateOrderInput,
  ExpertSystemInfo,
} from '@/types/api';

// Query keys
export const orderKeys = {
  all: ['orders'] as const,
  lists: () => [...orderKeys.all, 'list'] as const,
  list: (page: number) => [...orderKeys.lists(), { page }] as const,
  details: () => [...orderKeys.all, 'detail'] as const,
  detail: (id: string) => [...orderKeys.details(), id] as const,
  expertSystems: () => [...orderKeys.all, 'expert-systems'] as const,
  priceCalculation: () => [...orderKeys.all, 'price-calculation'] as const,
};

// Get all orders
export const useOrders = (page = 1, pageSize = 20) => {
  return useQuery({
    queryKey: orderKeys.list(page),
    queryFn: () => ordersApi.getAll(page, pageSize),
    staleTime: 5 * 60 * 1000, // 5 minutes
  });
};

// Get single order
export const useOrder = (id: string | undefined) => {
  return useQuery({
    queryKey: orderKeys.detail(id!),
    queryFn: () => ordersApi.getById(id!),
    enabled: !!id,
    staleTime: 5 * 60 * 1000,
  });
};

// Get available expert systems
export const useExpertSystems = () => {
  return useQuery({
    queryKey: orderKeys.expertSystems(),
    queryFn: () => ordersApi.getExpertSystems(),
    staleTime: 30 * 60 * 1000, // 30 minutes - expert systems change rarely
  });
};

// Calculate order price with discounts
export const useCalculatePrice = () => {
  return useMutation({
    mutationFn: (expertSystems: string[]) =>
      ordersApi.calculatePrice(expertSystems),
    onError: (error) => {
      console.error('Failed to calculate price:', getErrorMessage(error));
    },
  });
};

// Create order mutation
export const useCreateOrder = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (data: CreateOrderInput) => ordersApi.create(data),
    onSuccess: (newOrder) => {
      // Invalidate orders list to refetch
      queryClient.invalidateQueries({ queryKey: orderKeys.lists() });
      // Set the new order in cache
      queryClient.setQueryData(orderKeys.detail(newOrder.id), newOrder);
    },
    onError: (error) => {
      console.error('Failed to create order:', getErrorMessage(error));
    },
  });
};
