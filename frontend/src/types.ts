export interface User {
  id: number;
  username: string;
  email: string;
}

export interface Product {
  id: number;
  name: string;
  stock: number;
}

export interface Reservation {
  id: number;
  product_id: number;
  user_id: number;
  is_confirmed?: boolean | null;
}

export interface AuthToken {
  access_token: string;
  token_type: string;
}
