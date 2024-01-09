package mantova;

import robocode.*;
import robocode.util.*;
import static robocode.util.Utils.normalRelativeAngleDegrees;

public class TheBeast extends AdvancedRobot {
    private double last_scan_dist = 0;
    private double angle_absolute = 0;
    private double pos_enemy_x = 0;
    private double pos_enemy_y = 0;
    private int state = 0;
    private double moveAmount;
    private int sentido = 1;
    private double theta = 0;

    public void run() {
        moveAmount = Math.max(getBattleFieldWidth(), getBattleFieldHeight());

        setAdjustRadarForGunTurn(true);
        setAdjustRadarForRobotTurn(true);
        setAdjustGunForRobotTurn(true);

        turnRadarRight(Double.POSITIVE_INFINITY);  // Infinite radar rotation for continuous scanning

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
                    } else {
                        // rastreamento oscilatorio
                        this.state = 3;
                        turnGunRight(10);
                    }
                } else {
                    this.state = 4;
                    applyMeteoLocoEFoge();
                }
            }
            out.println("State: " + this.state);
        }
    }
    // O método para disparo preditivo
    private void predictiveShoot(ScannedRobotEvent e) {
        double bulletPower = Math.min(3.0, getEnergy() - .1);
        double bulletSpeed = 20 - bulletPower * 3;
        long time = (long)(last_scan_dist / bulletSpeed);

        double futureX = pos_enemy_x + Math.sin(angle_absolute) * e.getVelocity() * time;
        double futureY = pos_enemy_y + Math.cos(angle_absolute) * e.getVelocity() * time;
        double absDeg = (Math.toDegrees(Math.atan2(futureX - getX(), futureY - getY())) + 360) % 360;
        setTurnGunRight(normalRelativeAngleDegrees(absDeg - getGunHeading()));
        
        fire(bulletPower);
    }
    
        public void applySaindodeFininho(ScannedRobotEvent e) {
        int range = 10;
        ahead(20);
        if (getDistance() < range) {
            predictiveShoot(e);
        } else {
            // Scan para aglomerados e outros comportamentos 
        }
    }

    public void applyMeteoLocoEFoge() {
        turnLeft(getHeading() % 90);
        ahead(moveAmount);
        turnRight(90);
        turnGunRight(45);
    }

    public double getDistance() {
        return last_scan_dist;
    }

    public void onScannedRobot(ScannedRobotEvent e) {
        last_scan_dist = e.getDistance();
        angle_absolute = getHeadingRadians() + e.getBearingRadians();
        pos_enemy_x = getX() + Math.sin(angle_absolute) * e.getDistance();
        pos_enemy_y = getX() + Math.cos(angle_absolute) * e.getDistance();

        switch (this.state) {
            case 1: // mano a mano
                basicEnemyEngagement(e);
                break;

            case 2: // combate afastado
                applySaindodeFininho(e);
                break;

            case 3: // rastreamento oscilatorio
                advancedEnemyEngagement(e);
                break;

            case 4: // evasive action
                evasiveAction(e);
                break;
        }
    }

    private void basicEnemyEngagement(ScannedRobotEvent e) {
        // Regular aiming and shooting logic
        double bearingFromGun = normalRelativeAngleDegrees(e.getBearing() + getHeading() - getGunHeading());
        if (Math.abs(bearingFromGun) <= 3) {
            turnGunRight(bearingFromGun);
            if (e.getDistance() < 150) {
                fire(3);
            } else if (e.getDistance() < 300) {
                fire(2);
            } else {
                fire(1);
            }
        } else {
            turnGunRight(bearingFromGun);
        }
        if (bearingFromGun == 0) {
            scan();
        }
    }

    private void advancedEnemyEngagement(ScannedRobotEvent e) {
        setTurnRight(e.getBearing() + 90);
        ahead(40 * sentido);

        // Predictive shooting
        double bulletPower = Math.min(3.0, getEnergy() - .1);
        double bulletSpeed = 20 - bulletPower * 3;
        long time = (long)(last_scan_dist / bulletSpeed);

        // Predictive shot calculations
        double futureX = pos_enemy_x + Math.sin(angle_absolute) * e.getVelocity() * time;
        double futureY = pos_enemy_y + Math.cos(angle_absolute) * e.getVelocity() * time;
        double absDeg = (Math.toDegrees(Math.atan2(futureX - getX(), futureY - getY())) + 360) % 360;
        setTurnGunRight(normalRelativeAngleDegrees(absDeg - getGunHeading()));
        
        fire(bulletPower);
    }

    private void evasiveAction(ScannedRobotEvent e) {
        double bulletPower = e.getEnergy() / 4;
        setTurnRight(e.getBearing() + 90 - 30 * sentido);
        ahead((bulletPower + 2) * 15 * sentido);
        sentido *= -1;
        setTurnRadarRight(Double.POSITIVE_INFINITY);
    }

    public void onHitByBullet(HitByBulletEvent e) {
        setTurnRight(normalRelativeAngleDegrees(90 - (getHeading() - e.getHeading())));
        ahead(50);
    }

    public void onHitRobot(HitRobotEvent e) {
        if (e.getBearing() > -90 && e.getBearing() < 90) {
            back(100);
        } else {
            ahead(100);
        }
    }

    public void onHitWall(HitWallEvent e) {
        sentido *= -1;
        back(20);
        turnRight(180);
        ahead(20);
    }
}
