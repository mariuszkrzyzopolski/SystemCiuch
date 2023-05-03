import { Component, EventEmitter, Input, Output } from '@angular/core';
import { DTOCollectionItemDetails } from '../../model/DTOCollection';
import { SwiperOptions } from 'swiper';

@Component({
  selector: 'app-slider',
  templateUrl: './slider.component.html',
  styleUrls: ['./slider.component.css']
})
export class SliderComponent {
  _items: DTOCollectionItemDetails[];

  @Input() clothType: string;
  @Input() set items(i: DTOCollectionItemDetails[]) {
    this._items = i;
    if(i && i.length > 2) {
      this.currentId = i[1].id;
    }
  }
  @Input() showButtons: boolean = true;
  @Output() showDetailsEvent = new EventEmitter<DTOCollectionItemDetails>();
  @Output() showSettingsEvent = new EventEmitter<DTOCollectionItemDetails>();
  @Output() deleteEvent = new EventEmitter<DTOCollectionItemDetails>();
  //@Output() deleteEvent = new EventEmitter<DTOCollectionItemDetails>();

  get items(): DTOCollectionItemDetails[] {
    return this._items;
  }

  currentIndex: number = 1;
  currentId: number | null = null;
  config: SwiperOptions = {
    slidesPerView: 3,
    spaceBetween: 50,
    navigation: true,
    pagination: { clickable: true },
    scrollbar: { draggable: true },
  };
  
  onSlideNextTransitionEnd() {
    debugger;
    this.currentId = this._items[++this.currentIndex].id;
  }

  onSlidePrevTransitionEnd() {
    debugger;
   this.currentId = this._items[--this.currentIndex].id;
  }

  showSettings(item: DTOCollectionItemDetails) {
    this.showSettingsEvent.emit(item);
  }

  showDetails(item: DTOCollectionItemDetails) {
    this.showDetailsEvent.emit(item);
  }

  deleteItem(item: DTOCollectionItemDetails) {
    this.deleteEvent.emit(item);
  }
}
