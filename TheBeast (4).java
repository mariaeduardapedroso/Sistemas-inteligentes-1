package sample;

import robocode.*;
import robocode.util.*;
import java.awt.geom.*;
import robocode.ScannedRobotEvent;
import static robocode.util.Utils.normalRelativeAngleDegrees;

//import java.awt.Color;

// API help : https://robocode.sourceforge.io/docs/robocode/robocode/Robot.html

/**
 * TheBeast - a robot by (your name here
 */
public class TheBeast extends AdvancedRobot {
	/**
	 * run: TheBeast's default behavior
	 */
	private double last_scan_dist = 0;
	private double angle_absolute = 0;
	private double pos_enemy_x = 0;
	private double pos_enemy_y = 0;
	private int state = 0;
	private double moveAmount;
	private double next_pos_enemy_x = 0;
	private double next_pos_enemy_y = 0;
	private int sentido = 1;
	private int[] oscil = {0,1,0,-1,0};
	private int count = 0;


	public void run() {
		// Initialization of the robot should be put here
		// Initialize moveAmount to the maximum possible for this battlefield.
		moveAmount = Math.max(getBattleFieldWidth(), getBattleFieldHeight());
		// After trying out your robot, try uncommenting the import at the top,
		// and the next line:

		//setColors(new Color(255, 0, 0), new Color(0, 0, 255) ,new Color(0, 255, 0)); // body,gun,radar
		// setAdjustRadarForGunTurn(true);
		// setAdjustRadarForRobotTurn(true);
		setAdjustGunForRobotTurn(true);
		

		// Robot main loop
		while (true) {

			if (getOthers() == 1) {
				// mano a mano
				this.state = 1;
				turnGunRight(10);
			} else {
				if (getEnergy() > 25) {
					if (getEnergy() < 70) {
						// combate afastado
						this.state = 2;
						applySaindodeFininho();
					} else {
						this.state = 3;
						turnGunRight(10);
					}
				} else {
					this.state = 4;
					applyMeteoLocoEFoge();
				}

			}
		}
	}


	public void applySaindodeFininho() {
		// verifica inimigo perto do range
		int range = 10;
		ahead(20);
		if (getDistance() < range) {
			// mete bala
		} else {
			// scan para aglomerados

			// atira
		}

	}


	public void applyMeteoLocoEFoge() {
		// define um inicio e um destino
		// trabalhar com cantos??
		// define aleatoriedade do caminho
		turnLeft(getHeading() % 90);
		setTurnRadarRight(Double.POSITIVE_INFINITY);
		// Move up the wall
		ahead(moveAmount);
		// Turn to the next wall
		turnRight(90);
		turnGunRight(45);
	}

	public double getDistance() {
		double retorno = 0;
		switch (this.state) {
			case 1:
				retorno = this.last_scan_dist;
				break;
		}
		return retorno;

	}

	/**
	 * onScannedRobot: What to do when you see another robot
	 */
	public void onScannedRobot(ScannedRobotEvent e) {
		// Replace the next line with any behavior you would like

		switch (this.state) {
			case 1: // applyVemTranquilo
				
				// Vira o corpo para ele ou perpendicular
				if(e.getDistance() < 200){
					turnGunRight(e.getBearing());
					turnRight(e.getBearing() + 90*this.sentido);
					ahead(20);
				} else {
					turnGunRight(e.getBearing());
					turnRight(e.getBearing());
					ahead(e.getDistance() -200);
				}
				


				if (getGunHeat() == 0) {
					if (e.getDistance() < 150) {
						fire(3);
						// Caso ele estiver menor q 300 de distancia fogo nivel 2
					} else if (e.getDistance() < 300) {
						fire(2);
						// Caso distancia maior que 300 fogo nivel 1
					} else {
						fire(1);
					}
				}
							
				
				break;
			case 2: // applySaindodeFininho

				break;
			case 3: // applyCassadaCelwagem
			
				//Vira o corpo para onde o inimigo está
				if(e.getDistance() > 150){
					// Se o alvo está longe, chega perto
					turnGunRight(e.getBearing());
					turnRight(e.getBearing());
					ahead(e.getDistance() - 50);
				} else {
					// Se o alvo está perto, atira rodeando ele
					turnGunRight(e.getBearing());
					turnRight(e.getBearing() + 90*this.sentido);
					ahead(40);
				}
							
				
				if (getGunHeat() == 0) {
					if (e.getDistance() < 150) {
						fire(3);
						// Caso ele estiver menor q 300 de distancia fogo nivel 2
					} else if (e.getDistance() < 300) {
						fire(2);
						// Caso distancia maior que 300 fogo nivel 1
					} else {
						fire(1);
					}
				}
				
				
							

				break;
				
				case 4: // applyMeteoLocoEFoge

				// Calculate exact location of the robot
				double absoluteBearing = getHeading() + e.getBearing();
				double bearingFromGun = normalRelativeAngleDegrees(absoluteBearing - getGunHeading());
				turnGunRight(bearingFromGun);
				if (getGunHeat() == 0) {
					if (e.getDistance() < 150) {
						fire(3);
						// Caso ele estiver menor q 300 de distancia fogo nivel 2
					} else if (e.getDistance() < 300) {
						fire(2);
						// Caso distancia maior que 300 fogo nivel 1
					} else {
						fire(1);
					}
				}
				break;
		}

		// setTurnRadarLeft(getRadarTurnRemaining());
		// fire(1);
	}

	/**
	 * onHitByBullet: What to do when you're hit by a bullet
	 */
	public void onHitByBullet(HitByBulletEvent e) {
		// Replace the next line with any behavior you would like
		back(10);
	}

	/**
	 * onHitWall: What to do when you hit a wall
	 */
	public void onHitWall(HitWallEvent e) {
		// Replace the next line with any behavior you would like
		this.sentido = this.sentido*(-1);
	}
	

	

	public void onHitRobot(HitRobotEvent e) {
		if (e.isMyFault()) {
			setTurnLeft(70);
			back(70);
		} else {
			setTurnRight(70);
			ahead(70);
		}

	}

	public void onSkippedTurn(SkippedTurnEvent e) { // Funcao caso o robo skipe um turno
		turnRadarLeft(180);
		turnLeft(5);
		ahead(5);
	}

}
