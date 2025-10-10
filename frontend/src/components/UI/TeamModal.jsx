import React from 'react'
import { useGameStore } from '../../stores/gameStore'
import './TeamModal.css'

/**
 * Team Modal Component
 * Displays OrbitSowers Labs team information
 */
export default function TeamModal() {
  const showTeamModal = useGameStore(state => state.showTeamModal)
  const setShowTeamModal = useGameStore(state => state.setShowTeamModal)

  if (!showTeamModal) return null

  const onClose = () => setShowTeamModal(false)

  const teamMembers = [
    {
      name: 'Olivier Youfang Kamgang',
      role: 'Aerospace Engineering Student (CEP)',
      location: 'Montréal, Canada',
      linkedin: 'https://linkedin.com/in/olivier-youfang-kamgang',
      github: 'https://github.com/YkorTech',
      email: 'ykortech@gmail.com'
    },
    {
      name: 'Amaury Tchoupe',
      role: 'Mechanical Engineering Student (CEP)',
      location: 'Montréal, Canada',
      linkedin: 'https://linkedin.com/in/amaury-tchoupe-3b24ab190',
      github: 'https://github.com/Brivell',
      email: 'amaurytchoupe01@gmail.com'
    },
    {
      name: 'Mathurin Nkinassi',
      role: 'Financial Mathematics Student',
      location: 'Montréal, Canada',
      linkedin: 'https://linkedin.com/in/mathurin-nkinassi-b70b3b1a3',
      github: 'https://github.com/Nkinassi',
      email: 'nkinassimathurin@gmail.com'
    },
    {
      name: 'Oswald Godwill Litet',
      role: 'M.Eng Electrical Engineering',
      location: 'Montréal, Canada',
      linkedin: 'https://linkedin.com/in/oswald-godwill-litet-191a36223',
      github: 'https://github.com/oswald-litet',
      email: 'oswaldowill21@gmail.com'
    }
  ]

  return (
    <div className="team-modal-overlay" onClick={onClose}>
      <div className="team-modal" onClick={(e) => e.stopPropagation()}>
        <button className="team-modal-close" onClick={onClose}>×</button>

        <div className="team-modal-header">
          <img
            src="/assets/logos/orbitsowers_logo.png"
            alt="OrbitSowers Labs"
            className="team-modal-logo"
          />
          <h2>OrbitSowers Labs</h2>
          <p className="team-subtitle">From Yaoundé, Cameroon to Montréal, Canada</p>
          <p className="team-mission">
            "Cultivating the future with NASA's eyes in the sky"
          </p>
        </div>

        <div className="team-about">
          <h3>About the Challenge</h3>
          <p>
            The agriculture community faces the challenge of integrating technology and data to enhance
            sustainable farming practices. Simulating key farming activities like fertilizing, irrigating,
            and livestock management using real-world NASA satellite imagery and climate data can enable
            better understanding of the impacts of these variables on crop production. Your challenge is
            to create an engaging educational game that effectively utilizes NASA's open data sets to
            simulate farming scenarios and enables players to learn how this data can inform innovative,
            sustainable, agricultural methods.
          </p>
          <a
            href="https://www.spaceappschallenge.org/2025/challenges/nasa-farm-navigators-using-nasa-data-exploration-in-agriculture/"
            target="_blank"
            rel="noopener noreferrer"
            className="challenge-link"
          >
            Read Full Challenge Details →
          </a>
        </div>

        <div className="team-members">
          <h3>Team Members</h3>
          <div className="team-grid">
            {teamMembers.map((member, index) => (
              <div key={index} className="team-member-card">
                <div className="member-info">
                  <h4>{member.name}</h4>
                  <p className="member-role">{member.role}</p>
                  <p className="member-location">📍 {member.location}</p>
                </div>

                <div className="member-links">
                  <a
                    href={member.linkedin}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="member-link linkedin"
                    title="LinkedIn Profile"
                  >
                    <svg width="20" height="20" fill="currentColor" viewBox="0 0 24 24">
                      <path d="M19 0h-14c-2.761 0-5 2.239-5 5v14c0 2.761 2.239 5 5 5h14c2.762 0 5-2.239 5-5v-14c0-2.761-2.238-5-5-5zm-11 19h-3v-11h3v11zm-1.5-12.268c-.966 0-1.75-.79-1.75-1.764s.784-1.764 1.75-1.764 1.75.79 1.75 1.764-.783 1.764-1.75 1.764zm13.5 12.268h-3v-5.604c0-3.368-4-3.113-4 0v5.604h-3v-11h3v1.765c1.396-2.586 7-2.777 7 2.476v6.759z"/>
                    </svg>
                    LinkedIn
                  </a>

                  <a
                    href={member.github}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="member-link github"
                    title="GitHub Profile"
                  >
                    <svg width="20" height="20" fill="currentColor" viewBox="0 0 24 24">
                      <path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/>
                    </svg>
                    GitHub
                  </a>

                  <a
                    href={`mailto:${member.email}`}
                    className="member-link email"
                    title="Email"
                  >
                    <svg width="20" height="20" fill="currentColor" viewBox="0 0 24 24">
                      <path d="M0 3v18h24v-18h-24zm6.623 7.929l-4.623 5.712v-9.458l4.623 3.746zm-4.141-5.929h19.035l-9.517 7.713-9.518-7.713zm5.694 7.188l3.824 3.099 3.83-3.104 5.612 6.817h-18.779l5.513-6.812zm9.208-1.264l4.616-3.741v9.348l-4.616-5.607z"/>
                    </svg>
                    Email
                  </a>
                </div>
              </div>
            ))}
          </div>
        </div>

        <div className="team-footer">
          <p>
            <strong>NASA Space Apps Challenge 2025</strong> • Montréal Edition
          </p>
          <div className="team-links">
            <a
              href="https://www.spaceappschallenge.org/2025/find-a-team/orbitsowers-labs/?tab=project"
              target="_blank"
              rel="noopener noreferrer"
              className="team-footer-link nasa-link"
            >
              View Our NASA Space Apps Submission
            </a>
            <a
              href="https://github.com/YkorTech/OrbitSowers_TerraGrow"
              target="_blank"
              rel="noopener noreferrer"
              className="team-footer-link github-link"
            >
              View Project Repository
            </a>
          </div>
        </div>
      </div>
    </div>
  )
}
