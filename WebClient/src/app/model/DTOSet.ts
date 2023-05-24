export interface DTOSetItem {
  description: string;
  type: string;
  image: string;
  set_id: number | null;
  id: number;
  tags: string;
  collection_id: number;
}

export interface DTOSet {
  id: number;
  items: DTOSetItem[];
}