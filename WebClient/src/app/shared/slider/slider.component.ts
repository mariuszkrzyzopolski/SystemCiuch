import { Component, EventEmitter, Input, Output } from '@angular/core';
import { DTOCollectionItemDetails } from '../../model/DTOCollection';
import { SwiperOptions } from 'swiper';

@Component({
  selector: 'app-slider',
  templateUrl: './slider.component.html',
  styleUrls: ['./slider.component.css']
})
export class SliderComponent {
  @Input() clothType: string;
  @Input() items: DTOCollectionItemDetails[];
  @Input() showButtons: boolean = true;
  @Output() showDetailsEvent = new EventEmitter<DTOCollectionItemDetails>();
  @Output() showSettingsEvent = new EventEmitter<DTOCollectionItemDetails>();
  @Output() deleteEvent = new EventEmitter<DTOCollectionItemDetails>();

  config: SwiperOptions = {
    slidesPerView: 3,
    spaceBetween: 50,
    navigation: true,
    pagination: { clickable: true },
    scrollbar: { draggable: true },
  };
  
  onSlideChange() {
    console.log('slide change');
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
