import { Component, OnInit} from '@angular/core';
import { DTOCollectionItem, DTOCollectionItemDetails } from '../../../app/model/CollectionDTO';
;
import SwiperCore, { Navigation, Pagination, Scrollbar, A11y } from 'swiper';
import { CollectionService } from '../../../app/services/CollectionService';
SwiperCore.use([Navigation, Pagination, Scrollbar, A11y]);

@Component({
  selector: 'app-clothes-prviev',
  templateUrl: './clothes-preview.component.html',
  styleUrls: ['./clothes-preview.component.css'],
})
export class ClothesPreviewComponent implements OnInit {
  items: DTOCollectionItemDetails[];
  upperGarments: DTOCollectionItemDetails[];
  lowerGarments: DTOCollectionItemDetails[];
  footwear: DTOCollectionItemDetails[];
  detailsItem: DTOCollectionItemDetails | null = null;
  itemToRemove: DTOCollectionItemDetails | null = null;
  showModal = false;

  constructor(private collectionService: CollectionService) { }
  
  ngOnInit(): void {
    this.loadItems();
  }

  loadItems() {
    this.collectionService.getCollection().subscribe(data => {
      this.items = data.Collection.items;
      this.upperGarments = this.items.filter(item => item.type === 'Upper garment');
      this.lowerGarments = this.items.filter(item => item.type === 'Lower garment');
      this.footwear = this.items.filter(item => item.type === 'Footwear');
    });
  }
  showDetails(item: DTOCollectionItemDetails){
     this.detailsItem = item;
  }

  delete(item: DTOCollectionItemDetails) {
    this.itemToRemove = item;
    this.showModal = true;
  }

  cancelRemove() {
    this.showModal = false;
  }

  removeItem(){
    this.collectionService.deleteCollectionItem(this.itemToRemove!.id).subscribe(data =>  {
      this.showModal = false;
      this.loadItems();
    });
  }
}


