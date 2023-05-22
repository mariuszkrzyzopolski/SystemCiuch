export interface DTOCollection {
    Collection: DTOCollectionItem;
  }
  
  export interface DTOCollectionItem {
    id: number;
    items: DTOCollectionItemDetails[];
  }
  
  export interface DTOCollectionItemDetails {
    id: number;
    type: string;
    description: string;
    image: string;
    set_id: number | null;
    tags: string;
    collection_id: number;
  }