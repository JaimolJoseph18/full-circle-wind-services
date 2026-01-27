import { Card, Icon } from 'semantic-ui-react'
import { FC } from 'react'

interface StatCardProps {
  title: string;
  value: string | number;
  subText: string;
  icon: string;
  isAlert?: boolean;
}

export const StatCard: FC<StatCardProps> = ({ title, value, subText, icon, isAlert }) => (
  <Card fluid className="stat-card-white">
    <Card.Content>
      <div className="stat-card-content">
        <span className="stat-label">{title}</span>
        <Icon name={icon} className="stat-icon" />
      </div>
      <div className="stat-value-box">
        <h2 className={isAlert ? 'alert-text' : ''}>{value}</h2>
        <p className="stat-subtext">{subText}</p>
      </div>
    </Card.Content>
  </Card>
);