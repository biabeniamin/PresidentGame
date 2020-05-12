import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { GameComponent } from './game/game.component';
import { RouterModule } from '@angular/router';
import { CardComponent } from './card/card.component';
import { HttpClientModule } from '@angular/common/http';
import { PlayerComponent } from './player/player.component';

@NgModule({
  declarations: [
    AppComponent,
    GameComponent,
    CardComponent,
    PlayerComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    HttpClientModule,
    RouterModule.forRoot([
      { 
        path : '',
        component : GameComponent
      },
      { 
        path : 'game',
        component : GameComponent 
      },
      { 
        path : 'cards',
        component : CardComponent
      },
      { 
        path : 'control',
        component : PlayerComponent
      },
    ])
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
